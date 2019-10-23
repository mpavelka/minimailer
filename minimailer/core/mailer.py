import abc
import asab


class Mailer(asab.ConfigObject):

	ConfigDefaults = {
		'to': '',		# "john.doe@example.com:John Doe; another@mail.com;"
		'from': '',		# "john.doe@example.com:John Doe"
		'subject': '',	# "Subject"
	}

	def __init__(self, id, config=None):
		super().__init__(config_section_name="mailer:{}".format(id), config=config)
		self.Id = id


	@abc.abstractmethod
	def send_mail(self,
		text=None,
		html=None,
		config={}
	):
		raise NotImplemented()


	def parse_config_to(self, config):
		ret = []

		conf_to = config.get("to", self.Config["to"])
		if len(conf_to) == 0:
			raise ValueError("The 'to' option is empty.")

		for mail_name_pair in conf_to.split(";"):
			mail_name = mail_name_pair.split(":")
			if len(mail_name) == 1:
				ret.append({
					"mail": mail_name[0]
				})
			elif len(mail_name) == 2:
				ret.append({
					"mail": mail_name[0],
					"name": mail_name[1]
				})
			else:
				raise ValueError("Can't parse email and name from '{}'".format(mail_name))

		return ret


	def parse_config_from(self, config):
		ret = []

		conf_from = config.get("from", self.Config["from"])
		if len(conf_from) == 0:
			raise ValueError("The 'from' option is empty.")

		mail_name = conf_from.split(":")
		if len(mail_name) == 1:
			ret.append({
				"mail": mail_name[0]
			})
		elif len(mail_name) == 2:
			ret.append({
				"mail": mail_name[0],
				"name": mail_name[1]
			})
		else:
			raise ValueError("Can't parse email and name from '{}'".format(mail_name))

		return ret


