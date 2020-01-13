import asab
import aiohttp
import asab.web
import asab.web.rest
import re
import logging

import asab
from .sendgrid import SendGridModule
from .core.service import MinimailerService


###

L = logging.getLogger(__name__)

###


asab.Config.add_defaults({
	"mailer": {
		"engine": "sendgrid",
		"sendgrid_api_key": "",
		"to": "",
		"subject": ""
	}
})

class MinimailerApp(asab.Application):

	RAW_RE_EMAIL = r"\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,15})+"
	RAW_RE_NAME = r"\w+(\ \w+)*"

	# john.doe@example.com
	# john.doe@example.com:John Doe
	# john.doe@example.com:John Doe;john.doe@example.com;john.doe@example.com
	RE_TO = re.compile(r"^{re_email}(:{re_name})?(;{re_email}(:{re_name})?)?$".format(
		re_email=RAW_RE_EMAIL,
		re_name=RAW_RE_NAME
	))
	# john.doe@example.com
	# john.doe@example.com:John Doe
	RE_FROM = re.compile(r"^{re_email}(:{re_name})?$".format(
		re_email=RAW_RE_EMAIL,
		re_name=RAW_RE_NAME
	)) 


	def __init__(self):
		super().__init__()


		# Web module/service
		self.add_module(asab.web.Module)
		websvc = self.get_service('asab.WebService')

		# Minimailer service
		self.MinimailerService = MinimailerService(self)

		# Modules
		self.add_module(SendGridModule)

		# WEB
		#
		# Create a dedicated web container
		self.WebContainer = asab.web.WebContainer(websvc, 'minimailer:api')
		# JSON exception middleware
		self.WebContainer.WebApp.middlewares.append(asab.web.rest.JsonExceptionMiddleware)

		# ping
		self.WebContainer.WebApp.router.add_get('/ping', self.get_ping)

		# sendmail
		self.WebContainer.WebApp.router.add_post('/send/{mailer_id}', self.post_mail)


	async def get_ping(self, request):
		return asab.web.rest.json_response(
			request,
			{
				"ok": 1,
				"message": "pong"
			}
		)


	async def post_mail(self, request):
		mailer_id = request.match_info['mailer_id']
		mailer = self.MinimailerService.MailerRegistry.get(mailer_id)

		if mailer is None:
			raise aiohttp.web.HTTPNotFound(reason="Mailer with ID '{}' not registered.".format(mailer_id)) 

		try:
			mailer.send_mail(
				data=await request.json()
			)
		except Exception as e:
			L.error("Couldn't send email: {}".format(e))
			raise aiohttp.web.HTTPBadGateway()

		return asab.web.rest.json_response(
			request,
			{
				"ok": 1,
				"message": "mail sent"
			}
		)

