from minimailer.core import Mailer
from sendgrid import SendGridAPIClient

class SendGridMailer(Mailer):

	def __init__(self, id, config=None):
		super().__init__(id, config=None)
		self.Client = SendGridAPIClient(self.Config["sendgrid_api_key"])


	def send_mail(self,
		text=None,
		html=None,
		config={}
	):
		to_list = self.parse_config_to(config)
		from_dict = self.parse_config_from(config)
		subject = self.Config["subject"]


		data = {
			'personalizations': [
				{
					'to': to_list,
					'subject': subject
				}
			],
			'from': from_dict,
			'content': [
				{
					'type': 'text/plain',
					'value': text
				}
			],
			'mail_settings': {
				'sandbox_mode': {
					'enable': self.SandboxMode
				}
			}
		}


		self.Client.client.mail.send.post(
			request_body=data
		)
