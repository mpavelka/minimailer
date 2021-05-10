import asab
import aiohttp
import logging
import os
import python_http_client
from urllib.error import HTTPError

###

L = logging.getLogger(__name__)

###

asab.Config.add_defaults({
	"minimailer:api": {
		"listen": "{}:{}".format(
			os.getenv('HOST', "0.0.0.0"),
			os.getenv('PORT', "8080"),
		)
	}
})


class MinimailerRestHandler(object):

	def __init__(self, app):
		self.App = app
		self.WebService = app.get_service('asab.WebService')
		self.MinimailerService = app.get_service("minimailer.MinimailerService")

		# Create a dedicated web container
		self.WebContainer = asab.web.WebContainer(
			self.WebService,
			'minimailer:api'
		)

		# Apply JSON exception middleware to ensure
		# JSON responses for error states
		self.WebContainer.WebApp.middlewares.append(
			asab.web.rest.JsonExceptionMiddleware
		)

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

		# Respond with a 404 if there is no such
		# mailer with id $mailer_id
		if mailer is None:
			raise aiohttp.web.HTTPNotFound(
				reason="Mailer with ID '{}' not registered.".format(mailer_id)
			)

		# Send mail
		try:
			mailer.send_mail(
				data=await request.json()
			)
		except (
			HTTPError,
			python_http_client.exceptions.BadRequestsError
		) as e:
			L.error("Couldn't send email: {}: {}".format(e, e.body))
			raise aiohttp.web.HTTPBadGateway()

		except Exception as e:
			L.error("Couldn't send email: {}".format(e))
			raise aiohttp.web.HTTPBadGateway()

		# Email successfully sent
		# Respond with 200 OK
		return asab.web.rest.json_response(
			request,
			{
				"ok": 1,
				"message": "mail sent"
			}
		)
