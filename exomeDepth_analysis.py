from generic_utils.read_write_util import *
from Objects.GenericObject import *
from Objects.GenomicObject import *
from Objects.CNVObject import *
from analysis_utils.find_overlaps import find_interval_overlaps
from generic_utils.statistics_handlers import *
from analysis_utils.ucsc_genome_prep import prep_intervals_for_UCSCgenome_annotation

import sys




exomedepth_result_file = "/home/kbaeg/Documents/scripts/R/i_var/exomeDepth_13_pe.csv"
xhmm_result_file = "/home/kbaeg/Documents/outputs/run2/RUN2.cnv"
xhmm_filter_result_file = "/home/kbaeg/Documents/outputs/run2/FILTERED.cnv"
xhmm_denovo_result_file = "/home/kbaeg/Documents/outputs/run2/RUN2.denovo.format.cnv"


s = TableObject(filename="/home/kbaeg/Documents/outputs/exomeDepth/exomeDepth_13_pe_ucscGenome_output.csv", delim = "\t")
# print(s.get_data())
s.add_id('id')
print(s.print_data())


p = s.get_freq(["hg19.kgXref.geneSymbol", "hg19.knownGene.chrom"], print_freq = False)
for i, v in p.items():
	print(i[1])
	print('index: ', i, 'value: ', v)

sys.exit()



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

p = exomeDepth.raw_results.get_freq(['"type"'], print_freq = False)

for i, v in p.items():
    print('index: ', i, 'value: ', v)

sys.exit()


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

