import unittest

from minimailer.core.transformer import KeyValueArrayTransformer


class KeyValueArrayTransformerTest(unittest.TestCase):

	def setUp(self):
		self.KeyValueArrayTransformer = KeyValueArrayTransformer()

	def test_transform(self):
		expected = {
			"keyvaluearray": [
				{"key": "key1", "value": "value1"},
				{"key": "key2", "value": {
					"foo": "bar"
				}}
			]
		}
		result = self.KeyValueArrayTransformer.transform({
			"key1": "value1",
			"key2": {
				"foo": "bar"
			}
		})

		self.assertDictEqual(result, expected)
