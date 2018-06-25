IN PROGRESS

DATA ORGANIZATION

	- GenericObject
		- used to group multiple data objects together (organization purposes)

		- initialization

		- functions
			- set_data(dataname, content)
				- dataname - the name of the dataset
				- content - the data that will be associated with the dataname
			- list_data()
				- will list all datasets in the GenericObject
			- get_data(dataname) - will retrieve the dataset associated with dataname
			- del_data(dataname) - will remove the dataset associated with datanames
			- print_data(dataname, **kwargs) - will print the dataset. if a library object, will access print_data function. kwargs specified will be applied


	- TableObject

		- initialization
			- data - initialize the stored dataset through either of following
				- filename, delim
				- list of list dataset

		- Column functions
			- set_colname(oldcolname, newcolname) - will renames the oldcolname to newcolname
			- get_colnames() - returns list of column names in order which they're stored
			- set_colkeys(colnames) - colnames must be dict. Keys must be mandatory column type (ex. id, chr, start, end, type). Values must be the column in the dataset whose contents match the mandatory column type
				- Ex. TableObject.set_colkeys({"id":"ID#", "chr": "chromosome"})
			- get_colkeys() - returns dict of all dataset columns that have been matched to a mandatory column type
			- del_col(colname) - deletes colname

		- Data functions
			- sort_row(by_var, ascending = True, descending = False, view_only = False)
				- by_var - list of indices OR column names which you want to sort by
				- ascending - sorts vars in ascending order
				- descending - sorts vars in descending order
				- view_only - if False, will not change the stored dataset and only return a copy of the dataset sorted.
			- flatten(columns = [], view_only = False)
				- columns that have arrays as values in the order specified in columns.
					- Ex. columns = ["id", "multiple_matches"]
					- Ex. columns = [0, 1]
				- to concurrently flatten multiple columns synchronously, use "||" in between column names
					Ex. columns = ["id||multiple_matches"]
					Ex. columns = ["0||1"]
				- if no columns specified, all columns with arrays will be flattened in order

		- Statistics functions
			- get_num_rows() - returns number of rows in dataset
			- get_freq(columns)
				- columns - must be list or column names or column indices. will return AAA

		- Data handling
			- set_data(data)
				- sets the dataset as data. data must be list of list
			- get_data(**kwargs)
				- returns dataset
				- start, end - indicates a section of the data you wish to retrieve. must be integers
			- export_data(filename, **kwargs)
				- start, end - indicates a section of the data you wish to retrieve. must be integers
				- format - aligns columns for easy viewing
				- creates file at filename or dataset
			- print_data(format = True, **kwargs)
				- prints data to terminal
				- format - aligns all columns for easy viewing (may not be practical for datasets with too many columns)


	- GenomicObject

		- initialization
			- data - same as TableObject

			- colnames - must specify following mandatory column names
				- id, chr, start, end
				- Ex. colnames - {"id": "ID", "chr": "chromosome", "start": "STRT", "end": "E"}
	

	- CNVObject

		- initialization
			- data - same as TableObject

			- colnames - must specify following mandatory column names
				- id, chr, start, end, type
				- Ex. colnames - {"id": "ID", "chr": "chromosome", "start": "STRT", "end": "E", "type":"CNV_type"}
				- default CNV "type" values:
					- dup - ['dup', 'gain', 'duplication']
					- del - ['del', 'loss', 'deletion']
					- unk - ['unk']
				- type_values - must be dict. Keys will specify type of CNV (if dup, del, or unk make sure the key matches). This is how custom CNV types can be added. Values must be in list. These will be the dataset values that correspond with the CNV type

			- CNV functions
				- get_cnvType_values - returns dict of all CNV types and values specified
				- set_cnvType_values(values)
					- values must be dict. can update values for CNV types. refer to "type_values" parameter in initialization for specifics


ANALYSIS FUNCTIONS
	
	- find_interval_overlaps(ref_obj, compare_objects, **kwargs) - used to find overlaps between genomic data based on base pair overlaps
		- returns a GenomicObject (or CNVObject depending on the overlap analysis done)
		- ref_obj - must be a GenomicObject or CNVObject
			- if CNVObject, the CNV type can be used to find overlaps as well
		- compare_objects - these will be compared to ref_obj (but not between compare_objects) to find overlaps
			- can be list or single object
		- kwargs
			- match_CNV - boolean. option to make sure CNVs match when finding overlaps
			- add_stats - boolean. will add info on percentage of overlaps, ids of row in compare_objects matched to ref_obj (_w/_id), and # of matches (_freq). Each compare_object will generate 2 of these columns so that matches are not mixed.
			- threshold - float. the minimum percentage of overlap to qualify as a match (0 to 1)
			- relative_to_first - default = False. if True, will use overlap percentage in reference to length of segment in ref_obj. If False, the reference will be the length of the segment in the compare_object
			- overlap_colname - must be list that matches number and order of compare objects. default is "overlap@" where @ is an integer



get overlap

find overlaps

read write