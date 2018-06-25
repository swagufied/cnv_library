import re

class GenericObject:


	dataname_regex = re.compile('[, |\t\n\r;\'"]+$')

	def __init__(self):
		self.datatables = []
	"""
	SET DATA
	"""
	def set_data(self, dataname, content):
		if not self.dataname_regex.match(dataname):
			setattr(self, dataname, content)
			self.datatables.append(dataname)
			print('"{}" added to {}').format(dataname, self)
		else:
			raise Exception('data names cannot use tabs, returns, spaces, or ;,"')

	def list_data(self):
		return self.datatables

	def get_data(self, dataname):
		return getattr(self, dataname)

	def del_data(self, dataname):
		setattr(self, dataname, None)
		del self.datatables[self.datatables.index(dataname)]


	def print_data(self, dataname, **kwargs):

		called_data = getattr(self, dataname)

		try:
			called_data.print_data(**kwargs)
		except:
			print(called_data)


	