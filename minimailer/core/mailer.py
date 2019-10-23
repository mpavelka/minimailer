import abc
import asab

from .formatter import JsonTextFormatter


class Mailer(asab.ConfigObject):

	ConfigDefaults = {
		'to': '',		# "john.doe@example.com:John Doe; another@mail.com;"
		'from': '',		# "john.doe@example.com:John Doe"
		'subject': '',	# "Subject"
		'sandbox': 'false',
		'text_formatter': '',
		'html_formatter': '',
	}

	def __init__(self, id, config=None):
		super().__init__(config_section_name="mailer:{}".format(id), config=config)
		self.Id = id
		self.SandboxMode = self.Config["sandbox"].lower() == "true"

		if self.Config["text_formatter"] == "json":
			self.text_formatter = JsonTextFormatter()
		else:
			self.text_formatter = None


	@abc.abstractmethod
	def send_mail(self,
		data,
		config={}
	):
		raise NotImplemented()


	def parse_config_to(self, config):
		ret = []

		conf_to = config.get("to", self.Config["to"])
		if len(conf_to) == 0:
			raise ValueError("The 'to' option is empty.")

		for email_name_pair in conf_to.split(";"):
			email_name = email_name_pair.split(":")
			if len(email_name) == 1:
				ret.append({
					"email": email_name[0]
				})
			elif len(email_name) == 2:
				ret.append({
					"email": email_name[0],
					"name": email_name[1]
				})
			else:
				raise ValueError("Can't parse email and name from '{}'".format(email_name))

		return ret


	def parse_config_from(self, config):
		ret = {}

		conf_from = config.get("from", self.Config["from"])
		if len(conf_from) == 0:
			raise ValueError("The 'from' option is empty.")

		email_name = conf_from.split(":")
		if len(email_name) == 1:
			return {
				"email": email_name[0]
			}
		elif len(email_name) == 2:
			return {
				"email": email_name[0],
				"name": email_name[1]
			}
		else:
			raise ValueError("Can't parse email and name from '{}'".format(email_name))

