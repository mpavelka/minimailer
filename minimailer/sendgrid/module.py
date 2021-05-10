import asab
from .mailer import SendGridMailer


class SendGridModule(asab.Module):

	def __init__(self, app):
		super().__init__(app)
		self.MinimailerService = app.get_service("minimailer.MinimailerService")
		self._register_mailers()

	def _register_mailers(self):
		for section in asab.Config.sections():
			if not section.startswith("mailer:sendgrid:"):
				continue

			self.MinimailerService.register_mailer(
				SendGridMailer(
					id=section[7:]  # mailer:[sendgrid:id],
				)
			)
