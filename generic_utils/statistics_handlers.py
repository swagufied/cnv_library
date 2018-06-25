


def get_freq(table, columns):



	def get_value(d, keys):
		for key in keys:
			try:
				d = d[key]
			except:
				return None
		return d

	def set_value(d, keys, first):

		ds = d
		d = get_value(d, keys[:-1])

		# initialize new keys
		if not d:
			d = ds
			for k in keys[:len(keys)-2]:
				d[k] = {}
				d = d[k]
			d = 0

			d = ds

		if first:
			d[keys[-1]] = 0
		else:
			d[keys[-1]] += 1

	#get column ids
	freq_dict = {}
	keys = [table[0][i] for i in columns]

	for i in range(1, len(table)):
		row = table[i]

		last_child = row[len(columns) - 1]

		if get_value(freq_dict, keys):
			set_value(freq_dict, keys, False)
		else:
			set_value(freq_dict, keys, True)



	print(freq_dict)