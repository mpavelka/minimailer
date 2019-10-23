class JsonTextFormatter(object):

	def __init__(self):
		pass

	def format(self, data_dict):
		assert isinstance(data_dict, dict)

		output = ""
		for key, value in data_dict.items():
			output += "{}: {}\n".format(key, value)

		return output
