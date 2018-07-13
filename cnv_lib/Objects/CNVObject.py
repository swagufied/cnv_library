
from cnv_lib.Objects.GenomicObject import GenomicObject

class CNVObject(GenomicObject):


	def __init__(self, **kwargs):
		GenomicObject.__init__(self, **kwargs)

		if not 'type' in self.col:
			raise Exception('You must specify a type column in a CVNObject')
		
		self.type_values = {}
		self.type_values['dup'] = ['dup', 'gain', 'duplication']
		self.type_values['del'] = ['del', 'loss', 'deletion']
		self.type_values['unk'] = ['unk']

		if 'type_values' in kwargs:
			self.set_cnvType_values(kwargs['type_values'])

		self._check_colnames()

	def __repr__(self):

		try:
			return "CNVObject: \"{}\"".format(self.name)
		except:
			return "<{} instance at {}>".format(self.__module__, hex(id(self)))

	def get_cnvType_values(self):
		return self.type_values

	def set_cnvType_values(self, values):
		for key in values:
			self.type_values[key] = values[key]

def initialize_empty_CNVObject():
	EmptyCNVObject = CNVObject(data=[['chr','start','end','id', 'type']], colnames = {'chr':'chr','start':'start','end':'end','id':'id', 'type':'type'})
	EmptyCNVObject.del_col(['chr','start','end','id', 'type'])
	print(type(EmptyCNVObject))
	return EmptyCNVObject