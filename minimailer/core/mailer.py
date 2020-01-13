import abc
import asab
import re

from .formatter import JsonTextFormatter
from .transformer import KeyValueArrayTransformer


class Mailer(asab.ConfigObject):

	ConfigDefaults = {
		'to': '',
		# "john.doe@example.com:John Doe; another@mail.com;"
		# "$to" => apply "to" key from the data dict
		'cc': '',
		'bcc': '',
		
		'from': '',
		# "john.doe@example.com:John Doe"
		
		'subject': '',
		# "Subject"
		
		'sandbox': 'false',
		'data_transformer': '',
		'text_formatter': '',
		'html_formatter': '',
	}

	def __init__(self, id, config=None):
		super().__init__(config_section_name="mailer:{}".format(id), config=config)
		self.Id = id
		self.Params = {}
		self.SandboxMode = self.Config["sandbox"].lower() == "true"

		if self.Config["text_formatter"] == "json":
			self.text_formatter = JsonTextFormatter()
		else:
			self.text_formatter = None

		# Transformer
		if self.Config["data_transformer"] == "keyvaluearray":
			self.data_transformer = KeyValueArrayTransformer()
		else:
			self.data_transformer = None

	@abc.abstractmethod
	def send_mail(self, data):
		raise NotImplementedError

	def parse_params(self, data, extra={}):
		return {
			"from": self.parse_param_email("from", data, extra=extra),
			"to": self.parse_param_email_list("to", data, extra=extra),
			"cc": self.parse_param_email_list("cc", data, extra=extra),
			"bcc": self.parse_param_email_list("bcc", data, extra=extra),
		}

	def parse_param_email_list(self, key, data, extra={}):
		conf_to = extra.get(key, self.Config[key]).strip()
		if len(conf_to) == 0:
			return []

		conf_to = self._expand_variables(
			conf_to,
			data=data
		)

		param_to = []
		for email_name_pair in conf_to.split(";"):
			email_name_pair = email_name_pair.strip()

			if len(email_name_pair) == 0:
				continue

			param_to.append(
				self._parse_email(email_name_pair)
			)

		return param_to

	def parse_param_email(self, key, data, extra={}):
		param_from = extra.get(key, self.Config[key]).strip()
		if len(param_from) == 0:
			return {}

		param_from = self._expand_variables(
			param_from,
			data=data
		)

		return self._parse_email(param_from)

	def _parse_email(self, email_string):
		"""
			Expected value of email_string is 'john.doe@example.com:John Doe'
		"""
		email_string

		email_value = email_string.split(":")
		if len(email_value) == 1:
			return {
				"email": email_value[0]
			}
		elif len(email_value) == 2:
			return {
				"email": email_value[0],
				"name": email_value[1]
			}
		else:
			raise ValueError("Can't parse email and name from '{}'".format(email_value))

	def _expand_variables(self, string, data):
		"""
		Expands data variables
		  e.g. When data looks like {"to": "some@email.com"}
		  then config option "${to}" will be expanded to "some@email.com"
		"""
		output = string

		for placeholder in set(re.findall(r"\$\{.+\}", output)):
			varname = placeholder[2:-1]  # Getting rid of "${" and "}"
			output = re.sub(
				r"\$\{"+varname+r"\}",
				data.get(varname, ""),
				output
			)

		return output
