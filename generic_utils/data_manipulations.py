# merge
# append
# filter

from operator import itemgetter

def sort_row(table, index, descending=False):

	def typify(x, index):
		return_list = []
		for i in index:
			try:
				return_list.append(float(x[i]))
			except:
				return_list.append(str(x[i]))

		return return_list
	return sorted(table, key=lambda x: typify(x, index))

	# return sorted(table, key=lambda x: [try: float(x[i]) except: str(x[i]) for i in index])

	# this method is faster, but cannot account for str(int) columns
	# table.sort(key=itemgetter(*index), reverse=descending)
	# return table

#flattens arrays in column data in table. if len(array) = n, n rows will be added to the table
def flatten_table(table, col_index):

	new_table = [table[0]]

	for i in range(1, len(table)):

		col_list = table[i][col_index[0]]

		if isinstance(col_list, list):

			# make sure all arrays have the same length
			compare_len = len(col_list)
			for index in col_index:
				if len(table[i][index]) != compare_len:
					raise Exception('Some columns you wish to concurrently flatten have arrays of different lengths. Ex. row_num = {}'.format(i))

			for m in range(0, len(col_list)):
				new_row = table[i][:]
				for index in col_index:
					new_row[index] = table[i][index][m]
				new_table.append(new_row)
		else:
			new_table.append(table[i])

	return new_table

def unflatten_table():
	return
	
def append_tables(TableObject1, TableObject2):
	return

def merge_col(TableObject1, TableObject2, columns):
	return

