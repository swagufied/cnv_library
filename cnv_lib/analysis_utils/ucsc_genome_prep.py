from generic_utils.value_manipulations import clean_string
from Objects.GenomicObject import GenomicObject
from Objects.CNVObject import CNVObject
from generic_utils.read_write_util import write_file


"""
formats intervals of a table to use for gene annotation in the link below.


http://genome.ucsc.edu/cgi-bin/hgTables
"""

def prep_intervals_for_UCSCgenome_annotation(GenomicData, return_list= False, save_results = True, filename = "ucsc_interval_prep_data.txt"):


	if not isinstance(GenomicData, (GenomicObject, CNVObject)):
		raise Exception("you must intput a GenomicObject or CNVObject.")

	data = GenomicData.get_data()

	# print(data[0])
	chr = GenomicData._get_colindex(GenomicData.get_colkeys()['chr'])
	start = GenomicData._get_colindex(GenomicData.get_colkeys()['start'])
	end = GenomicData._get_colindex(GenomicData.get_colkeys()['end'])

	formatted_data = [[data[0][chr], data[0][start], data[0][end]]]
	# print(formatted_data)

	for i in range(1, len(data)):
		formatted_data.append([clean_string(data[i][chr]), clean_string(data[i][start]), clean_string(data[i][end])])


	if save_results:
		write_file(filename, formatted_data, delim="\t")
		print('Genome intervals prepared for UCSC annotation. Go to "http://genome.ucsc.edu/cgi-bin/hgTables" and paste the intervals in.')
		return
	else:
		if return_list:
			return formatted_data
		else:

			formatted_data_string = ""

			for row in formatted_data:
				formatted_data_string += ("\t".join(row) + "\n")

			return formatted_data_string[:-1]

	