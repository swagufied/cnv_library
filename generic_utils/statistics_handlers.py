


# def get_freq(table, columns):



# 	def get_value(d, keys):
# 		for key in keys:
# 			try:
# 				d = d[key]
# 			except:
# 				return None
# 		return d

# 	def set_value(d, keys, first):

# 		ds = d
# 		d = get_value(d, keys[:-1])
# 		print(d)

# 		# initialize new keys
# 		if not d:
# 			print('here2')
# 			d = ds
# 			print(keys[:len(keys)-2])
# 			# for k in keys[:len(keys)-2]:

# 				d[k] = {}
# 				d = d[k]
# 			d = 0

# 			d = ds

# 		if first:
# 			d[keys[-1]] = 0
# 		else:
# 			d[keys[-1]] += 1

# 	#get column ids
# 	freq_dict = {}
# 	keys = [table[0][i] for i in columns]
# 	print(keys)

# 	for i in range(1, len(table)):
# 		row = table[i]
# 		print(row)
# 		last_child = row[len(columns) - 1]

# 		if get_value(freq_dict, keys):
# 			print('here')
# 			set_value(freq_dict, keys, False)
# 		else:
# 			set_value(freq_dict, keys, True)


# 		break
# 	print(freq_dict)


def get_freq(table, columns):


	def set_value(table, freq, colindex, last):


		if freq_table.get(row[col_index]):
			if last:
				freq[1] += 1
			else:
				set_value()

		return

	col_indices = []
	freq_dict = {}

	for column in columns:
		if isinstance(column, int):
			col_indices.append(column)
		else:
			col_indices.append(table[0].index(column))


	for i in range(1, len(table)):

		row = table[i]

		first_freq = freq_dict.get(col_index[0])

		# if the column value appeared for the first time
		if not first_freq and len(col_index) > 1:
			freq_dict[row[col_index[0]]] = {}
		elif not first_freq:
			freq_dict[row[col_index[0]]] = 1

		# if the column value had already appeared
		else:
			set_value(table, colindex)



	print(freq_dict)
