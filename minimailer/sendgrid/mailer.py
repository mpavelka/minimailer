from minimailer.core import Mailer
from sendgrid import SendGridAPIClient

class SendGridMailer(Mailer):

	def __init__(self, id, config=None):
		self.ConfigDefaults.update({
			"sendgrid_api_key": "",
			"template_id": "",
		})
		super().__init__(id, config=None)
		self.Client = SendGridAPIClient(self.Config["sendgrid_api_key"])
		self.template_id = self.Config["template_id"] if len(self.Config["template_id"]) > 0 else None


	def send_mail(self,
		data,
		config={}
	):
		to_list = self.parse_config_to(config)
		from_dict = self.parse_config_from(config)
		subject = self.Config["subject"]


		body = {
			'personalizations': [
				{
					'to': to_list,
					'subject': subject
				}
			],
			'from': from_dict,
			'mail_settings': {
				'sandbox_mode': {
					'enable': self.SandboxMode
				}
			}
		}

		if self.data_transformer is not None:
			data = self.data_transformer.transform(data)

		if self.template_id is not None:
			# TODO: Configurable validation rules for 'data'
			body['personalizations'][0]['dynamic_template_data'] = data
			body['template_id'] = self.template_id

		elif self.text_formatter is not None:
			body.update({
				'content': [
					{
						'type': 'text/plain',
						'value': self.text_formatter.format(data)
					}
				]
			})

		self.Client.client.mail.send.post(
			request_body=body
		)
