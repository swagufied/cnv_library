import re

def convert_to_int(intstring):

	intstring = str(intstring).lower()
	# replace any chr
	chr_removed = intstring.replace('chr', '')

	# replace any X or Y
	x_removed = chr_removed.replace('x', '23')
	y_removed = x_removed.replace('y','24')


	return int(re.findall('\d+', y_removed)[0])