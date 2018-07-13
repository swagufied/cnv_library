from analysis_utils.find_overlaps import find_interval_overlaps
from Objects.GenomicObject import GenomicObject, initialize_empty_GenomicObject
from Objects.CNVObject import CNVObject, initialize_empty_CNVObject

def annotate(base_obj, annotation_obj):

	if not isinstance(annotation_obj, list):
		annotation_obj = [annotation_obj]

	#validate objects are GenomicObject or CNVObject
	if isinstance(base_obj, (GenomicObject, CNVObject)):
		for obj in annotation_obj:
			if not isinstance(annotation_obj, (GenomicObject, CNVObject)):
				raise Exception("Annotation objects can only be GenomicObject or CNVObject")
			if not 'gene_id' in obj.get_colkeys:
				raise Exception("Every annotation_obj must have a \"gene_id\" column specified. Use GenomicObject.set_colkeys() to do this.")
	else:
		raise Exception("Annotation objects can only be GenomicObject or CNVObject")

	AnnotatedObject = initialize_empty_GenomicObject()

	i = 0
	overlap_colnames = []
	del_cols = []
	for obj in annotation_obj:
		overlap_colnames.append('annotated{}'.format(i))
		del_cols.append('annotated{}_w/_id'.format(i))
		del_cols.append('annotated{}_freq'.format(i))
		del_cols.append('annotated{}'.format(i))
		i += 1

	AnnotatedObject = find_interval_overlaps(base_obj, annotation_obj, AnnotatedObject, overlap_colnames = overlap_colnames, exclude_nonmatches = False,
			threshold=0, relative_to_first = True, add_stats = True)

	data = AnnotatedObject.get_data()
	

	annotated_data = [data[0].extend(['annotated_genes'])]
	
	for i in range(1, len(data)):
		
		row = data[i]
		row.append([])

		count = 0
		for id in row[data[0].index('annotated{}_w/_id'.format(count))]:
			gene_data = annotation_obj[count].get_data()
			for row2 in gene_data:
				if id == row2[gene_data[0].index(annotation_obj[count].get_colkeys['id']):
					row[-1].extend(row2[gene_data[0].index(annotation_obj[count].get_colkeys['gene_id']])
					break

		annotated_data.append(row)
		count += 1
		
	AnnotatedObject.del_col(del_cols)

	return AnnotatedObject