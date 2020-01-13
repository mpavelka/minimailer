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


	def send_mail(self, data, extra={}):

		params = self.parse_params(
			data=data,
			extra=extra
		)

		if len(params["to"]) == 0:
			raise ValueError("'to' is empty.")
		if len(params["from"]) == 0:
			raise ValueError("'from' is empty.")

		subject = self.Config["subject"]

		body = {
			'personalizations': [
				{
					'to': params["to"],
					'subject': subject
				}
			],
			'from': params["from"],
			'mail_settings': {
				'sandbox_mode': {
					'enable': self.SandboxMode
				}
			}
		}
		# CC
		if len(params["cc"]) > 0:
			body['personalizations'][0]['cc'] = params["cc"]
		# BCC
		if len(params["bcc"]) > 0:
			body['personalizations'][0]['bcc'] = params["bcc"]


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
