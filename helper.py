def print_table(titles, data, column_width=10):
	row_format = "|" + ("{:>" + str(column_width) + "}|") * len(data)

	data_new = []
	for i in xrange(len(data[0])):
		s = []
		for x in data:
			s.append(x[i])
		data_new.append(s)

	title = row_format.format(*titles)
	width_table = len(title)
	horiz_sep = "-" * width_table

	print horiz_sep
	print title
	print horiz_sep

	for row in data_new:
		print row_format.format(*row)

	print horiz_sep