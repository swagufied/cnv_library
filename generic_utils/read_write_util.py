import os
import uuid
import sys

# rewrites file with new delim. if output file is specified, new delim is written on new file
# all multiple spaces will be reduced to one space
def change_delim(filename, pre_delim, post_delim, **kwargs):

	multidelim = False
	if 'multidelim' in kwargs:
		multidelim = kwargs['multidelim']

	contents = read_file(filename, pre_delim, multidelim=multidelim)

	new_contents = [str(post_delim.join(row)) for row in contents]
			
	outfile=""
	if 'outfile' in kwargs:
		outfile = str(kwargs['outfile'])
	else:
		outfile = filename
	file = open(outfile, 'w+')

	for row in new_contents:
		file.write(str(row) + "\n")

	file.close()

	print('{} delim changed from "{}" to "{}"'.format(filename, pre_delim,post_delim))
	print('output: {}'.format(outfile))

# returns list of rows in data with each row as an array separated by delim
def read_file(filename, delim, **kwargs):

	file = open(filename,'r')
	contents = file.readlines()
	file.close()

	new_contents=[]
	# if 'multidelim' in kwargs and kwargs['multidelim']:
	for row in contents:
		split_row = row.strip().split(delim)

		clean_row = []
		if 'secondary_delim' in kwargs:
			clean_row = [col.strip().split(kwargs[secondary_delim]) for col in split_row]
		else:
			clean_row = [col.strip().split() for col in split_row]
		new_contents.append(clean_row)
	# else:
	# 	new_contents = [row.strip().split(delim) for row in contents]

	print('{} records read from {}'.format(len(contents) - 1, filename))
	print('-------------------------------------')
	return new_contents

def read_file_asDict(filename, delim, **kwargs):

	file = open(filename,'r')
	contents = file.readlines()
	file.close()

	new_contents = []
	col_row = {}
	for col in contents[0]:
		row[col] = contents[0].index(col)

	new_contents.append(col_row)

	for i in range(1, len(contents)):
		row = contents[i]
		new_row = {}

		for col in col_row:
			new_row[col] = row[col_row[col]]
		new_contents.append(new_row)

	return new_contents

# writes contents to file with delim specified
def write_file(filename, contents, delim, **kwargs):

	file = open(filename, 'w+')

	if isinstance(contents, str):
		file.write(str(contents))
		print('{} lines written to {}'.format(contents.count('\n'), filename))
	else:

		for row in contents:
			
			if 'secondary_delim' in kwargs:
				for col in row:
					col = kwargs['secondary_delim'].join(col)

			file.write(str(delim.join(row)) + "\n")
		print('{} lines written to {}'.format(len(contents), filename))
	file.close()

	print('-----------------------------------------------')


# returns array of contents filtered by cols
# kwargs specifes whether cols are index (boolean) and if they 
# specify desired columns (desired = boolean)
def filter_columns(contents, cols, **kwargs):
	
	desired = kwargs['desired']
	index = kwargs['index']

	if not isinstance(cols, list):
		terminate('cols must be presented in a list')
	elif kwargs['index']:
		for col in cols:
			try:
				contents[0][col]
			except:
				terminate('SOME INDEXES ARE OUT OF BOUNDS')

			if not isinstance(int(col),int):
				terminate('IF INDEX IS TRUE, cols must be INT')
	elif not kwargs['index']:
		for col in cols:
			try:
				contents[0].index(col)
			except:
				terminate('col "{}" doesnt exist or the first row doesnt have column names'.format(col))

	col_indexes = []
	if not index:
		col_indexes = [contents[0].index(str(col)) for col in contents[0] if col in cols]
		
	else:
		col_indexes = [int(col) for col in cols]
	col_indexes.sort()

	numcols = len(contents[0])

	filtered_contents = []
	for row in contents:

		new_row = []
		for i in range(0,numcols):
			
			if i in col_indexes and desired:
				new_row.append(row[i])
			elif not desired and not i in col_indexes:
				new_row.append(row[i])

		filtered_contents.append(new_row)

	return filtered_contents

#terminates code after printing error msg
def terminate(message):
	print(message)
	sys.exit()