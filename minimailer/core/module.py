import asab
from .service import MinimailerService
from .rest import MinimailerRestHandler


class MinimailerCoreModule(asab.Module):

	def __init__(self, app):
		super().__init__(app)
		self.MinimailerService = MinimailerService(self)
