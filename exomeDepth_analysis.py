from generic_utils.read_write_util import *
from Objects.GenericObject import *
from Objects.GenomicObject import *
from Objects.CNVObject import *
from analysis_utils.find_overlaps import find_interval_overlaps
from generic_utils.statistics_handlers import *

import sys




exomedepth_result_file = "/home/kbaeg/Documents/scripts/R/exomeDepth_calls.csv"
xhmm_result_file = "/home/kbaeg/Documents/outputs/run2/RUN2.cnv"
xhmm_filter_result_file = "/home/kbaeg/Documents/outputs/run2/FILTERED.cnv"
xhmm_denovo_result_file = "/home/kbaeg/Documents/outputs/run2/RUN2.denovo.format.cnv"


ss = read_file("/home/kbaeg/Documents/scripts/R/i_var/exomeDepth_13_pe.csv", ",")

output = []
for row in ss:
	chr = row[6].replace('"',"")

	output.append([chr, row[4], row[5]])

write_file("ss.txt", output, "\t")

sys.exit()

# table = [
# ['col1', 'col2', 'col3'],
# ['cat', 'healthy', 'bob'],
# ['cat', 'healthy', 'mark'],
# ['cat', 'sick', 'joe']
# ]
# get_freq(table, [1,'col3'])
# sys.exit()

# denovo = read_file(xhmm_denovo_result_file, "\t")
# denovo[0].append("ID")
# denovo[0].append("CHR")
# denovo[0].append("START")
# denovo[0].append("END")

# idcount = 1
# for i in range(1, len(denovo)):
# # for i in range(1, 10):
# 	row = denovo[i]
# 	row.append(str(idcount))
# 	idcount += 1

# 	splitrow = row[2].split(':')
# 	row.append(splitrow[0])

# 	splitrow2 = splitrow[1].split('..')
# 	row.append(splitrow2[0])
# 	row.append(splitrow2[1])

# 	cnvleft = row[3].split('<')
# 	cnvright = cnvleft[1].split('>')
# 	row[3] = cnvright[0]

# 	print(row)

# write_file("/home/kbaeg/Documents/outputs/run2/RUN2.denovo.format.cnv", denovo, "\t")



# sys.exit()


exomeDepth = GenericObject()
tofind_overlaps = []

# for i in range(2,12):
# 	filename = "/home/kbaeg/Documents/scripts/R/i_var/exomeDepth_{}_pe.csv".format(i)
# 	exomeDepth_result = CNVObject(filename = filename, delim=",", 
# 		colnames = {'id': '"id"', 'chr':'"chromosome"', 'start':'"start"', 'end':'"end"', 'type':'"type"'})
# 	exomeDepth.set_data('results_{}'.format(i), exomeDepth_result)
# 	if i != 2:
# 		tofind_overlaps.append(getattr(exomeDepth, 'results_{}'.format(i)))

# tofind_overlaps = [exomeDepth.results_8]
# total_overlap = find_interval_overlaps(exomeDepth.results_10, tofind_overlaps, threshold = 0, add_stats = True, match_CNV = True)
# print(total_overlap.print_data())

# sys.exit()

#create exomeCopyDepth object
exomeDepth = GenericObject()
print('jsfdo')
exomeDepth_genomic_obj = CNVObject(filename = exomedepth_result_file, delim=",", 
	colnames = {'id': '"id"', 'chr':'"chromosome"', 'start':'"start"', 'end':'"end"', 'type':'"type"'})
exomeDepth.set_data('raw_results', exomeDepth_genomic_obj)

#create xhmm object
xhmm = GenericObject()
xhmm_raw_data = GenomicObject(filename = xhmm_result_file, delim = "\t",
	colnames = {'id':'FID', 'chr':'CHR', 'start':'BP1', 'end':'BP2'})
xhmm_filter_data = GenomicObject(filename = xhmm_filter_result_file, delim = "\t",
	colnames = {'id':'FID', 'chr':'CHR', 'start':'BP1', 'end':'BP2'})
xhmm_denovo_data = CNVObject(filename = xhmm_denovo_result_file, delim = "\t",
	colnames = {'id': 'ID', 'chr':'CHR', 'start':'START', 'end':'END', 'type':'CNV'})
xhmm.set_data('raw_results', xhmm_raw_data)
xhmm.set_data('filtered_results', xhmm_filter_data)
xhmm.set_data('denovo', xhmm_denovo_data)


tofind_overlaps = [xhmm.denovo, xhmm.filtered_results]
overlap1 = find_interval_overlaps(exomeDepth.raw_results, tofind_overlaps, threshold=0, add_stats=True)

print(overlap1.print_data(start=1, end=3))

# overlap1.flatten(columns=['overlap1||overlap1_w/_id'])
overlap1.flatten(columns=["13||14"])
overlap1.export_data("sss.txt", format=True, start = 0, end = 3,delim=",")

# print(overlap1.print_data())

sys.exit()



overlap1 = find_overlaps(exomeDepth_obj, xhmm_obj, threshold=0, add_stats=True)
overlap2 = find_overlaps(exomeDepth_obj, xhmm_filter_obj, threshold=0, add_stats=True)

print(overlap1.get_num_rows())
print(overlap2.get_num_rows())


# overlap.print_data()

print(exomeDepth_obj.get_colnames())
exomeDepth_obj.print_data(start=1, end=5)

