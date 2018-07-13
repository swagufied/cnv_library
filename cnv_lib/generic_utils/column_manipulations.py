
def delete_column(content, del_index):

	new_content = []

	for row in content:
		del row[del_index]

		new_content.append(row)

	return new_content