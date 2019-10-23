import asab
from .service import SendGridService

class SendGridModule(asab.Module):
	def __init__(self, app):
		super().__init__(app)
		SendGridService(app)
