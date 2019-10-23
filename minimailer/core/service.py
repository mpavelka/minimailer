from abc import abstractmethod
import asab


class MinimailerService(asab.Service):

	def __init__(self, app, service_name="minimailer.MinimailerService"):
		super().__init__(app, service_name)
		self.MailerRegistry = {}


	def register_mailer(self, mailer):
		if mailer.Id in self.MailerRegistry:
			raise RuntimeError("Mailer with id '{}' already registered.")

		self.MailerRegistry[mailer.Id] = mailer
