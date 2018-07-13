from cnv_lib.generic_utils.value_manipulations import list_to_lower, clean_string

def check_CNV_match(CNVObject1, cnv_value1, CNVObject2, cnv_value2):
	values1 = CNVObject1.get_cnvType_values()
	values2 = CNVObject2.get_cnvType_values()

	#make sure same key exists in both objects
	key1 = None
	for key in values1:
		if clean_string(cnv_value1.lower()) in list_to_lower(values1[key]):
			key1 = key.lower()
			break
	# print(key1)
	key2 = None
	for key in values2:
		if clean_string(cnv_value2.lower()) in list_to_lower(values2[key]):
			key2 = key.lower()
			break

	#see which key the value is associated with
	if key1 != key2:
		return False
	else:
		return True

	#check if the keys match