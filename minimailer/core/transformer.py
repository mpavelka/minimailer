
class KeyValueArrayTransformer(object):

	def __init__(self):
		pass

	def transform(self, data):
		res = []
		for key, value in data.items():
			res.append({
				"key": key,
				"value": value
			})
		return {
			"keyvaluearray": res
		}
