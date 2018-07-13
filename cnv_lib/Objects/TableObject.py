import cnv_lib.generic_utils.read_write_util as FileHandler
import cnv_lib.generic_utils.column_manipulations as ColManip
import cnv_lib.generic_utils.data_manipulations as DataManip
import re
import pandas as pd


class TableObject:

	def __init__(self,**kwargs):
		#read in file if filename is given
		if 'filename' in kwargs:
			self.delim = kwargs['delim']

			if 'secondary_delim' in kwargs:
				self.data = FileHandler.read_file(kwargs['filename'], delim=kwargs['delim'], secondary_delim=kwargs['secondary_delim'])
			else:
				self.data = FileHandler.read_file(kwargs['filename'], delim=kwargs['delim'])
		else:
			self.data = kwargs['data']

		if 'name' in kwargs:
			self.name = kwargs['name']

		# print(self.data[0])
		if 'headers' in kwargs:
			if not isinstance(kwargs['headers'], list):
				raise Exception('Headers must be input as a list!')

			if len(kwargs['headers']) != len(self.get_data()[0]):
				raise Exception('Length of the header list doesnt match the number of columns!')

			self.data.insert(0, kwargs['headers'])

		self.col = {}

		if 'colnames' in kwargs:
			self.set_colkeys(kwargs['colnames'])

		self._check_colnames()

	def __repr__(self):

		try:
			return "TableObject: \"{}\"".format(self.name)
		except:
			return "<{} instance at {}>".format(self.__module__, hex(id(self)))

	"""
	COLUMN HANDLERS
	"""
	#these are used to maintain necessary columns
	def set_colkeys(self, colnames):
		for name in colnames:
			self.col[name] = colnames[name]
		self._check_colnames()
	def get_colkeys(self):
		return self.col

	#these are used to keep track of data thats actually presented
	def set_colname(self, oldcolname, newcolname):
		colindex = self._get_colindex(oldcolname)
		data[0][colindex] = newcolname
	def get_colnames(self):
		return self.data[0]
	
	def _get_colindex(self, colname):

		try:
			colname = int(colname)
			return colname
		except:
			return self.data[0].index(colname)
	# TODO: def set_colindex
	def _check_colnames(self):
		for colname in self.col:
			if not self.col[colname] in self.data[0]:
				raise Exception('"{}" does not exist in {}'.format(self.col[colname], self))
	# TODO: def change_colorder():
	def del_col(self, colname):

		if isinstance(colname, list):
			for col in colname:
				ColManip.delete_column(self.data, self._get_colindex(col))
		else:
			ColManip.delete_column(self.data, self._get_colindex(colname))

	"""
	DATA FUNCTIONS
	"""
	def add_id(self, colname):

		self.set_data(DataManip.add_id(self.data, colname))
		self.set_colkeys({'id': colname})


	# sorts column(s) by ascending or descending order. default = ascending
	def sort_row(self, by_var, ascending=True, descending=False, view_only = False, **kwargs):
		if not ascending:
			descending = True
		if not isinstance(by_var, list):
			raise Exception('"by_var" argument input must be a list')

		indices = []
		for var in by_var:
			if isinstance(var, int):
				indices.append(var)
			else:
				indices.append(self._get_colindex(var))

		tempdata = [self.data[0]]
		tempdata.extend(DataManip.sort_row(self.data[1:len(self.data)], indices, descending=descending))

		if view_only:
			return tempdata
		else:
			self.data=tempdata
			return self.data

	# renders all array contents on separate rows
	def flatten(self, columns = [], view_only = False, exclude = False):
		tempdata = self.data

		if columns:
			for column in columns:
				col_index = [column]
				if isinstance(column, str):
					split_col = column.split('||')

					col_index = [self._get_colindex(i) for i in split_col]
				tempdata = DataManip.flatten_table(tempdata, col_index)
		else:
			for i in range(0, len(self.get_colnames())):
				tempdata = DataManip.flatten_table(tempdata, i)

		if view_only:
			return tempdata
		else:
			self.data = tempdata
			return self.data

	"""
	STATISTICS HANDLERS
	"""
	def get_num_rows(self):
		return len(self.data) - 1
	def get_freq(self, columns, print_freq=True):

		colnames = []

		for column in columns:
			if isinstance(column, str) and column in self.data[0]:
				colnames.append(column)

			elif isinstance(column, int):
				colnames.append(self.data[0][column])
			else:
				raise Exception("You must provide only column names or column indices as strings or integers respectively when specifying columns for a function.")

		df = pd.DataFrame(self.data[1:], columns = self.data[0])
		freq = df.groupby(columns, as_index = False).size()

		if print_freq:
			print('-----------------------------------------------')
			print("\"get_freq\" RESULTS")
			print('-----------------------------------------------')
			print("columns = {}".format(', '.join(columns)))
			print(' ')
			print(freq)
			print('-----------------------------------------------')
		else:

			freq_dict = {}

			for i, v in freq.items():

				temp_key = freq_dict

				for key in i:
					if key != i[len(i) - 1]:

						temp_key[key] = {}

						temp_key = temp_key[key]
					else:
						temp_key[key] = v

				# print(temp_key)

			return freq_dict

	def get_col_values(self, columns, print_values = True):

		if not isinstance(columns, list):
			raise Exception('Input columns for get_col_values() must be list')

		header = []
		indices = []
		for column in columns:
			if isinstance(column, str):
				column = self._get_colindex(column)

			indices.append(column)
			header.append(self.data[0][column])

		values = [header]
		for row in self.data[1:]:

			temp_row = []
			for column in indices:
				temp_row.append(row[column])

			if not temp_row in values:
				values.append(temp_row)

		if print_values:
			self.print_data(data=values)
			return
		else:
			return values

	"""
	DATA HANDLERS
	"""
	def set_data(self, data):
		self.data = data

	# returns data or subsections if start and end are specified
	def get_data(self, **kwargs):

		start = 1
		if 'start' in kwargs:
			start = kwargs['start']
			if start <= 0:
				start = 1

		end = len(self.data)
		if 'end' in kwargs:
			end = kwargs['end']

		return_data = [self.data[0]]
		return_data.extend(self.data[start:end])

		return return_data

	#writes data to a designated file
	def export_data(self, filename, format=False, **kwargs):

		
		if format:
			string = self._format_data(**kwargs)
			FileHandler.write_file(filename, string, "")
			print("data successfully writtent to \"{}\"".format(filename))
			return

		start = 1
		if 'start' in kwargs:
			start = int(kwargs['start'])
			if start <= 0:
				start = 1

		end = len(self.data)
		if 'end' in kwargs:
			end = int(kwargs['end'])

		write_data = [self.data[0]]
		write_data.extend(self.data[start:end])

		if not 'delim' in kwargs:
			FileHandler.write_file(filename, write_data, self.delim)
		else:
			FileHandler.write_file(filename, write_data, kwargs['delim'])

	# prints data in terminal
	def print_data(self, format = True, data = None, **kwargs):

		if not data:
			data = self.data

		start = 1
		if 'start' in kwargs:
			start = int(kwargs['start'])
			if start <= 0:
				start = 1

		end = len(data)
		if 'end' in kwargs:
			end = int(kwargs['end'])
		
		if format:
			print(self._format_data(data, **kwargs))
		else:
			print(data[0])
			for i in range(start, end):
				print(data[i])

		print "{} rows printed".format(end - start + 1)
	
	# returns string of datatable that is formatted for neat columns
	def _format_data(self, data, **kwargs):

		start = 1
		if 'start' in kwargs:
			start = int(kwargs['start'])
			if start <= 0:
				start = 1

		end = len(data)
		if 'end' in kwargs:
			end = int(kwargs['end'])
		
		col_widths = {}

		format_end = 10
		if end < 10:
			format_end = end

		for row in data[0:format_end]:
			for i in range(0, len(row)):

				if len(str(row[i])) > col_widths.get(i):
					col_widths[i] = len(str(row[i]))
		
		formatted_string = "".join(str(data[0][i]).ljust(col_widths[i] + 2) for i in range(0, len(data[0]))) + "\n"
		for row in data[start:end+1]:
			formatted_string += "".join(str(row[i])[0:col_widths[i]].ljust(col_widths[i] + 2) for i in range(0, len(row))) + "\n"

		return formatted_string[:-1]
		