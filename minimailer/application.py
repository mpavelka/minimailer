import asab
import aiohttp
import asab.web
import asab.web.rest
import re

import asab
from .sendgrid import SendGridModule
from .core.formatter import JsonTextFormatter


asab.Config.add_defaults({
	"mailer": {
		"engine": "sendgrid",
		"sendgrid_api_key": "",
		"to": "",
		"subject": ""
	}
})

class MinimailerApp(asab.Application):

	RE_EMAIL = re.compile(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,15})+$")

	def __init__(self):
		super().__init__()

		# Web module/service
		self.add_module(asab.web.Module)
		websvc = self.get_service('asab.WebService')

		# Mail providers
		self.add_module(SendGridModule)
		self.sendgrid_client_id = asab.Config["mailer"]["sendgrid_api_key"]
		self.SendGridService = self.get_service('minimailer.SendGridService')
		self.SendGridService.create_client(
			id=self.sendgrid_client_id,
			api_key=asab.Config["mailer"]["sendgrid_api_key"]
		)

		# Create a dedicated web container
		self.WebContainer = asab.web.WebContainer(websvc, 'minimailer:api')
		# JSON exception middleware
		self.WebContainer.WebApp.middlewares.append(asab.web.rest.JsonExceptionMiddleware)

		# ping
		self.WebContainer.WebApp.router.add_get('/ping', self.get_ping)

		# sendmail
		self.WebContainer.WebApp.router.add_post('/send', self.post_mail)


	async def get_ping(self, request):
		return asab.web.rest.json_response(
			request,
			{
				"ok": 1,
				"message": "pong"
			}
		)


	async def post_mail(self, request):
		request_json = await request.json()

		data_from = request_json.get("from")
		if not isinstance(data_from, dict):
			raise aiohttp.web.HTTPBadRequest("There must be a field 'from' of type dictionary in the request json.")
		
		from_mail = data_from.get("mail", "")
		if re.match(self.RE_EMAIL, from_mail) is None:
			raise aiohttp.web.HTTPBadRequest("Invalid email address in 'from.mail'.")

		data_json = request_json.get("json")
		if not isinstance(data_json, dict):
			raise aiohttp.web.HTTPBadRequest("There must be a field 'json' of type dictionary in the request json.")

		# To
		to_mail = asab.Config["mailer"]["to"]
		subject = asab.Config["mailer"]["subject"]
			
		self.SendGridService.send_mail(
			client_id=self.sendgrid_client_id,
			from_dict={
				"mail": from_mail
			},
			to_list=[
				{"mail": to_mail}
			],
			subject=subject,
			text=JsonTextFormatter().format(data_json)
		)

		return asab.web.rest.json_response(
			request,
			{
				"ok": 1,
				"message": "mail sent"
			}
		)

