
from util.constants import *
from util.ped_func import get_affected, add_siblings_to_filteredcnv
from util.cnvfile_func import filter_cnvfile, read_cnvfile
from util.famfile_func import filter_famfile_by_patid
from util.decipher_func import read_decipher
from util.file_func import cnv
from util.dgv_func import read_dgv, find_common_cnv
from util.read_write_util import *
from util.annotate import *

import subprocess
import sys
 

"""
look at all cnvs detected by xhmm protocol 1. filters out cnvs if more than 2 ppl (in total pop and affected pop) have the cnv.
"""


thresh_num = 12
minscore = 60


denovofile = ROOT + "/RUN2.cnv"
r = read_file(denovofile, '\t')

newdenovo = []
for row in r:
	newdenovo.append(['chr{}'.format(row[2]), row[3], row[4]])

w = write_file('all_intervals.txt', newdenovo, '\t')
sys.exit()


"""
see if cnvs match with those in databases
"""
#check against dgv and decipher
outfile = "OUTPUT.txt"
outfile2 = FILTERED + ".cnv"

temput = 'temp.txt'
count = 0
count2 = 0
temparray = []
g = read_file(str(OUTPUT) + ".aff.cnv", '\t')
for t in g:
	if t[5] == '1':
		count += 1
	else:
		temparray.append(t)
		try:
			if int(t[6]) < 50:
				count2 += 1
		except:
			pass

write_file(temput, temparray, '\t')

print(count)
print(count2)
sys.exit()
# decipher = read_decipher(DECIPHER)
# cnv_file = read_cnvfile(CNVFILE, delim="\t")
# dgv = read_dgv()

# matches = find_common_cnv(cnv_file, decipher, 'Decipher', threshold=0.7)
# matches2 = find_common_cnv(matches, dgv, 'DGV', threshold=0.7)
# write_file(outfile, matches2, "\t")



# filter out patients who have been matched to common cnvs

x = read_file(outfile, "\t")
pat_ids = []
temp = [x[0]]
for i in x[1:len(x)]:
	if int(i[8]) <= 0:
		temp.append(i)
		pat_ids.append(i[0])


# convert file to same format as XHMM_OUTPUT
exclude = ['TOTAL_MATCH', 'Decipher_OVERLAP', 'Decipher_ID', 'DGV_OVERLAP', 'DGV_ID']

filtered = filter_columns(temp, exclude, index=False, desired = False)
unique_ids = list(set(pat_ids))


write_file(outfile2, filtered, "\t")

# t 


# create new fam file
filtered_fam = FILTERED + ".fam"
filter_famfile_by_patid(str(FAMFILE), filtered_fam, unique_ids)

call = "{0} --cfile {1} --cnv-make-map --noweb --out {1}".format(str(PLINK), str(FILTERED))
subprocess.call(call, shell=True)



"""
only take cnv call if occuring in less than 2 ppl. cohort = everyone
"""
root = str(OUTPUT) + '.all'

filter_output = root + ".max_{}".format(thresh_num)
call = "{0} --cfile {1} --cnv-freq-exclude-above {2} --noweb --cnv-overlap 0.5 --cnv-write --out {3}".format(str(PLINK), str(FILTERED), thresh_num, str(filter_output))
subprocess.call(call,shell=True)

#ensure minscore
minscore_output = filter_output + ".minSQ{0}".format(minscore)
filter_cnvfile(cnv(filter_output), cnv(minscore_output), delim=" ", minscore = minscore)


#check if any siblings have matching cnv
all_sibling_output = minscore_output + ".sib"
add_siblings_to_filteredcnv(cnv(minscore_output), cnv(all_sibling_output), str(PED), delim=" ")


# sys.exit()



"""
only take cnv call if occuring in less than 2 ppl. cohort = affected
"""
root = str(OUTPUT) + ".aff"

#get affected patids
affected_pats = get_affected(PED) 

# generate new cnv file of affected patients
filter_cnvfile(str(FILTERED_CNV), cnv(root), delim = "\t",pat_ids=affected_pats)

#generate new cnv map file of affected patients
call = "{0} --cfile {1} --cnv-make-map --noweb --out {1}".format(str(PLINK), str(root))
subprocess.call(call, shell=True)


# generate new map file of affected patients
aff_fam = root + ".fam"
filter_famfile_by_patid(str(FILTERED_FAM), str(aff_fam), affected_pats)


#cnv occurs in <= 2??
filter_output = root + ".max_{}".format(thresh_num)
call = "{0} --cfile {1} --cnv-freq-exclude-above {2} --noweb --cnv-overlap 0.5 --cnv-write --out {3}".format(str(PLINK), str(root), thresh_num, filter_output)
subprocess.call(call,shell=True)


#ensure minscore
minscore_output = filter_output + ".minSQ{0}".format(minscore)
filter_cnvfile(cnv(filter_output), cnv(minscore_output), delim=" ", minscore = minscore)

#check if any siblings have matching cnv
aff_sibling_output = minscore_output + ".sib"
add_siblings_to_filteredcnv(cnv(minscore_output), cnv(aff_sibling_output), str(PED), delim=" ")


"""
ANNOTATE INTERVALS
"""

outfile = '/home/kbaeg/Documents/data_sets/cnvs/annotated/hg19_fullexome.id.txt'
# assign_id_toannotation(annotated_exome, outfile)

# for cohort = everyone
print(all_sibling_output)
sibcnv_output = cnv(all_sibling_output)
cnv_read = read_file(sibcnv_output, ' ')

cnv_converted = convert_XY(cnv_read, 'CHR')

annotation = read_annotation(outfile)

exclude = ['SIBLINGS', 'SIB_IN_LIST', 'SIB_MATCH_ID', 'OVERLAP']
filtered = filter_columns(cnv_converted, exclude, index=False, desired = False)

results = annotate(filtered, annotation, 'SSV5', threshold=0.7)
write_file(sibcnv_output + ".annotated",results,'\t')


# for cohort = affected
sibcnv_output = cnv(aff_sibling_output)
cnv_read = read_file(sibcnv_output, ' ')

cnv_converted = convert_XY(cnv_read, 'CHR')
annotation = read_annotation(outfile)

exclude = ['SIBLINGS', 'SIB_IN_LIST', 'SIB_MATCH_ID', 'OVERLAP']
filtered = filter_columns(cnv_converted, exclude, index=False, desired = False)

results = annotate(filtered, annotation, 'SSV5', threshold=0.7)
write_file(sibcnv_output + ".annotated",results,'\t')

