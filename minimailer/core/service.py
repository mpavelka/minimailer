import asab


class MinimailerService(asab.Service):

	def __init__(self, app, service_name="minimailer.MinimailerService"):
		super().__init__(app, service_name)

		# Key-value registry of mailers
		# where key is a user-defined mailer id
		# and value a MailerEngine id
		self.MailerRegistry = {}

	def register_mailer(self, mailer):
		"""Registers a mailer"""

		if id in self.MailerRegistry:
			raise RuntimeError("Mailer with ID '{}' already registered.")

		self.MailerRegistry[mailer.Id] = mailer
