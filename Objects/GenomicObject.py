
from Objects.TableObject import TableObject

class GenomicObject(TableObject):

	def __init__(self, **kwargs):
		TableObject.__init__(self, **kwargs)
		
		required_cols = ['chr','start','end','id'] 

		check_required_cols = [i for i in set(required_cols).intersection(set(self.col.keys()))]
		if len(check_required_cols) != 4:
			raise Exception('You must have "chr", "start", "end", and "id" columns specifed in a GenomicObject')

		self._check_colnames()

	# def _initialize_empty_GenomicObject(self):
	# 	EmptyGenomicObject = GenomicObject(data=[['chr','start','end','id']], colnames = {'chr':'chr','start':'start','end':'end','id':'id'})
	# 	EmptyGenomicObject.del_col(['chr','start','end','id'])
	# 	return EmptyGenomicObject

	# def find_overlaps(self, compare_objects, **kwargs):

	# 	if isinstance(compare_objects, list):
	# 		print('here')
	# 		for compare_object in compare_objects:
	# 			if not isinstance(compare_object, GenomicObject):
	# 				raise Exception('Only GenomicObjects can be used in "find_overlaps"')

	# 		input_data = self
			

	# 		for compare_object in compare_objects:
	# 			EmptyGenomicObject = self._initialize_empty_GenomicObject()
	# 			print(compare_object.get_num_rows())
	# 			input_data = FindOverlaps.find_overlaps(input_data, compare_object, EmptyGenomicObject, **kwargs)
	# 			print(input_data.get_num_rows())
	# 		return input_data
	# 	else:
	# 		EmptyGenomicObject = self._initialize_empty_GenomicObject()
	# 		return FindOverlaps.find_overlaps(self, compare_objects, EmptyGenomicObject, **kwargs)

	

def initialize_empty_GenomicObject():
	EmptyGenomicObject = GenomicObject(data=[['chr','start','end','id']], colnames = {'chr':'chr','start':'start','end':'end','id':'id'})
	EmptyGenomicObject.del_col(['chr','start','end','id'])
	return EmptyGenomicObject

	



# class ExomeObject(GenomicObject):
# 	def __init__(self):

# 	def __str__(self):
# 		return 