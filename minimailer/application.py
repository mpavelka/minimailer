import asab
import asab.web
import asab.web.rest
import logging

import asab
from .core.service import MinimailerService
from .core.rest import MinimailerRestHandler


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

	def __init__(self):
		super().__init__()

		# Web module/service
		self.add_module(asab.web.Module)

		# Minimailer service
		self.MinimailerService = MinimailerService(self)

		# REST handler
		self.MinimailerRestHandler = MinimailerRestHandler(self)

		# Modules
		for engine in self._get_mailer_engines_from_config():
			if engine == "sendgrid":
				from .sendgrid import SendGridModule
				self.add_module(SendGridModule)

	def _get_mailer_engines_from_config(self):
		engines = set([])

		for section in asab.Config.sections():
			parts = section.split(":")
			if parts[0] != "mailer" or len(parts) < 2:
				continue
			
			engines.add(parts[1])

		return engines
