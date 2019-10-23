import os
import aiohttp
import asab
import logging
import hashlib
from sendgrid import SendGridAPIClient

###

L = logging.getLogger(__name__)

###

class SendGridService(asab.Service):

	def __init__(self, app, service_name="minimailer.SendGridService"):
		super().__init__(app, service_name)
		self._clients = {}


	def create_client(self,
		id,
		api_key
	):
		if id in self._clients:
			raise RuntimeError("Ignoring attempt to re-create a SendGridClient with previously used api_key.")

		self._clients[id] = SendGridAPIClient(api_key)


	def send_mail(self,
		client_id,
		from_dict,
		to_list,
		subject="",
		text=None,
		html=None
	):
		print("Client: {}".format(self._clients[client_id]))
		print("From: {}".format(from_dict))
		print("To:".format(to_list))
		print("Text:")
		print(text)
		print("HTML:")
		print(html)
