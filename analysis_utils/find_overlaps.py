
from generic_utils.type_conversions import convert_to_int
from generic_utils.cnv_utils import check_CNV_match
from Objects.GenomicObject import GenomicObject, initialize_empty_GenomicObject
from Objects.CNVObject import CNVObject, initialize_empty_CNVObject
import sys




def find_interval_overlaps(ref_obj, compare_objects, **kwargs):

	# kwargs: add_stats, overlap_colname, relative_to_first
	def _find_overlaps(GenomicObject1, GenomicObject2, ReturnGenomicObject, match_CNV=False, add_stats=False, relative_to_first=False, threshold = 0, **kwargs):
		genomic_object1_data = GenomicObject1.get_data()
		genomic_object2_data = GenomicObject2.get_data()

		#determine if overlap statistics along with 
		if add_stats:
			count = 1
			while(('overlap{}'.format(count)).strip() in genomic_object1_data[0]):
				count += 1

			overlap_freq = "overlap{}_freq".format(count)
			overlap_colname = "overlap{}".format(count)
			overlap_with_colname = "overlap{}_w/_id".format(count)
			if 'overlap_colname' in kwargs:
				overlap_freq = "{}_freq".format(kwargs['overlap_colname'])
				overlap_colname = kwargs['overlap_colname']
				overlap_with_colname = "{}_w/_id".format(kwargs['overlap_colname'])

			genomic_object1_data[0].append(overlap_freq)
			genomic_object1_data[0].append(overlap_colname)
			genomic_object1_data[0].append(overlap_with_colname)

		#initialize new data
		data = [genomic_object1_data[0]]

		#determine all indexes necessary
		genomic_object1_chr_index   = GenomicObject1._get_colindex(GenomicObject1.col["chr"])
		genomic_object1_start_index = GenomicObject1._get_colindex(GenomicObject1.col["start"])
		genomic_object1_end_index   = GenomicObject1._get_colindex(GenomicObject1.col["end"])
		genomic_object1_id_index    = GenomicObject1._get_colindex(GenomicObject1.col["id"])

		genomic_object2_chr_index   = GenomicObject2._get_colindex(GenomicObject2.col["chr"])
		genomic_object2_start_index = GenomicObject2._get_colindex(GenomicObject2.col["start"])
		genomic_object2_end_index   = GenomicObject2._get_colindex(GenomicObject2.col["end"])
		genomic_object2_id_index    = GenomicObject2._get_colindex(GenomicObject2.col["id"])

		genomic_object1_type_index = None
		genomic_object2_type_index = None

		if match_CNV:
			genomic_object1_type_index = GenomicObject1._get_colindex(GenomicObject1.col["type"])
			genomic_object2_type_index = GenomicObject2._get_colindex(GenomicObject2.col["type"])


		#find the overlaps
		for row1 in genomic_object1_data[1:len(genomic_object1_data)]:

			overlap_list = [] 
			id_list = []

			for row2 in genomic_object2_data[1:len(genomic_object2_data)]:
				#make sure chromosome matches
				if convert_to_int(row1[genomic_object1_chr_index]) != convert_to_int(row2[genomic_object2_chr_index]):
					continue
				#make sure CNV type matches
				if match_CNV:
					if not check_CNV_match(GenomicObject1, row1[genomic_object1_type_index], GenomicObject2, row2[genomic_object2_type_index]):
						continue


				row1_start = convert_to_int(row1[genomic_object1_start_index])
				row1_end   = convert_to_int(row1[genomic_object1_end_index])
				row2_start = convert_to_int(row2[genomic_object2_start_index])
				row2_end   = convert_to_int(row2[genomic_object2_end_index])

				overlap = _calculate_overlap(row1_start, row1_end, row2_start, row2_end, threshold, relative_to_first)

				if overlap:
					overlap_list.append(overlap)
					id_list.append(row2[genomic_object2_id_index])

			if len(overlap_list) >= 1:
				if add_stats:
					row1.append(str(len(overlap_list)))
					row1.append(overlap_list)
					row1.append(id_list)
					data.append(row1)

				else:
					data.append(row1)

		ReturnGenomicObject.set_data(data)
		ReturnGenomicObject.set_colkeys(GenomicObject1.get_colkeys())
		return ReturnGenomicObject

	# checks if two cnv intervals overlap and returns the greatest percentage of overlap in refernece to either interval
	def _calculate_overlap(start, end, cstart, cend, threshold, relative_to_first):

		overlap = -1
		if start <= cstart and cstart < end:
			start_0 = 0
			end_0 = end - start
			cstart_0 = cstart - start
			cend_0 = cend - start

			if cend_0 <= end_0:
				overlap = 1
			else:
				o1 = (end_0 - cstart_0)/float(end_0 - start_0)
				o2 = (end_0 - cstart_0)/float(cend_0 - cstart_0)
				
				if o1 >= o2 or relative_to_first:
					overlap = o1
				else:
					overlap = o2

		elif start >= cstart and cend > start:
			start_0 = start - cstart
			end_0 = end - cstart
			cstart_0 = 0
			cend_0 = cend - cstart
			

			if cend_0 >= end_0:
				overlap = 1
			else:
				o1 = (cend_0 - start_0) / float(end_0 - start_0)
				o2 = (cend_0 - start_0) / float(cend_0 - cstart_0)

				if o1 >= o2 or relative_to_first:
					overlap = o1
				else:
					overlap = o2

		if overlap > threshold:
			
			return round(overlap,4)
		else:
			return False

	# main body
	print("comparing {} to {}".format(ref_obj, compare_objects))

	if 'match_CNV' in kwargs and kwargs['match_CNV']:
		if not isinstance(ref_obj, CNVObject):
			raise Exception('In order to match CNV types in determining overlap, you must use CNVObjects')

	#check inputs
	if isinstance(compare_objects, list):
		for compare_object in compare_objects:
			if not isinstance(compare_object, (CNVObject, GenomicObject)):
				raise Exception('Only GenomicObjects and CNVObjects can be used in "find_overlaps"')

			if 'match_CNV' in kwargs and kwargs['match_CNV']:
				if not isinstance(compare_object, CNVObject):
					raise Exception('In order to match CNV types in determining overlap, you must use CNVObjects')

		if 'overlap_colnames' in kwargs:
			if isinstance(compare_objects, list):
				if len(kwargs['overlap_colnames']) != len(compare_objects):
					raise Exception('number of "overlap_colnames" and inputs is different!')
			else:
				raise Exception('"overlap_colnames" argument must be a list if overlap comparison inputs is a list')


	elif isinstance(compare_objects, (CNVObject, GenomicObject)):
		if 'overlap_colnames' in kwargs:
			if len(kwargs['overlap_colnames']) == 1:
				pass
			else:
				raise Exception('Single comparisons in checking for overlap must take 1 list item for custom "overlap_colname"')

		if 'match_CNV' in kwargs and kwargs['match_CNV']:
			if not isinstance(compare_objects, CNVObject):
				raise Exception('In order to match CNV types in determining overlap, you must use CNVObjects')

	else:
		raise Exception('Only GenomicObjects or lists of GenomicObjects can be used in "find_overlaps"')


	

	#start checking for overlaps
	if isinstance(compare_objects, list):
		
		input_data = ref_obj
		
		if 'overlap_colnames' in kwargs:

			for compare_object, colname in zip(compare_objects, kwargs['overlap_colnames']):
				EmptyGenomicObject = None

				if 'match_CNV'in kwargs and kwargs['match_CNV']:
					EmptyGenomicObject = initialize_empty_CNVObject()
				else:
					EmptyGenomicObject = initialize_empty_GenomicObject()

				input_data = _find_overlaps(input_data, compare_object, EmptyGenomicObject, overlap_colname = colname, **kwargs)
			return input_data

		else:

			for compare_object in compare_objects:
				EmptyGenomicObject = None

				if 'match_CNV'in kwargs and kwargs['match_CNV']:
					EmptyGenomicObject = initialize_empty_CNVObject()
				else:
					EmptyGenomicObject = initialize_empty_GenomicObject()

				input_data = _find_overlaps(input_data, compare_object, EmptyGenomicObject, **kwargs)
			return input_data

	else:
		EmptyGenomicObject = None

		if 'match_CNV'in kwargs and kwargs['match_CNV']:
			EmptyGenomicObject = initialize_empty_CNVObject()
		else:
			EmptyGenomicObject = initialize_empty_GenomicObject()

		return _find_overlaps(ref_obj, compare_objects, EmptyGenomicObject, **kwargs)

#checks for any column contents that overlap
def find_column_overlaps():
	return