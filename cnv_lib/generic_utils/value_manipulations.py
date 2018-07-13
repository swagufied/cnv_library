import re

def list_to_lower(input_list):
	return_list = []

	for content in input_list:
		if isinstance(content, list):
			return_list.append(list_to_lower(content))
		else:
			return_list.append(content.lower())

	return return_list

def clean_string(input_string):
	return re.sub('[!@#$"]', '', input_string)