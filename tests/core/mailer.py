import unittest

from minimailer.core.mailer import Mailer


class MailerTest(unittest.TestCase):

	def test_parse_params_01(self):
		mailer = Mailer("test", {
			"from": "john.doe@example.com:John Doe",
			"to": "john.doe@example.com:John Doe; ${from};",
			"bcc": "test@test.com"
		})

		expected = {
			"from": {
				"email": "john.doe@example.com",
				"name": "John Doe"
			},
			"to": [
				{
					"email": "john.doe@example.com",
					"name": "John Doe"
				},
				{
					"email": "another@mail.com",
				}
			],
			"cc": [],
			"bcc": [
				{
					"email": "test@test.com",
				}
			],
		}

		result = mailer.parse_params(
			data={
				"from": "another@mail.com",
				"to": "IRELEVANT"
			},
		)

		self.assertDictEqual(expected, result)
