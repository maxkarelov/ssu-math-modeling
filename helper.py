def print_vertical_table(titles, data, column_width=25, print_lists_to_file=0):
    row_format = "|" + ("{:>" + str(column_width) + "}|") * len(data)

    # Reorganize data array
    data_new = []
    for i in xrange(len(data[0])):
        s = []
        for x in data:
            s.append(x[i])
        data_new.append(s)

    title = row_format.format(*titles)
    width_table = len(title)
    horiz_sep = "-" * width_table

    # Printing
    print horiz_sep
    print title
    print horiz_sep

    for row in data_new:
        print row_format.format(*row)

    print horiz_sep

    # Writing to file
    if print_lists_to_file:
        file = open("values.txt", 'w') 
        file.write(str(data[0]) + '\n')
        file.write(str(data[1]))
        file.close()

def print_table(titles_x, titles_y, data, column_width=5):
    nx = len(titles_x)
    ny = len(titles_y)

    row_format = "|" + ("{:>" + str(column_width) + "}|") * (nx + 1)

    title = row_format.format("", *titles_x)
    width_table = len(title)
    horiz_sep = "-" * width_table

    # Printing
    print horiz_sep
    print title
    print horiz_sep

    for i in range(0, ny):
        print row_format.format(titles_y[i], *data[i])

    print horiz_sep

def frange(x, y, jump):
    while x < y:
      yield x
      x += jump


class DividedDiffirence:

    __dd_array = []

    def __init__(self, xs, ys):
        self.xs = xs
        self.ys = ys

        n = len(self.xs)
        for i in range(0, n):
            self.__dd_array.append([])
            for j in range(0, n):
                self.__dd_array[i].append("")

        self.__fill_table()

    def __str__(self):
        n = len(self.xs)
        #self.__fill_table()

        titles_x = titles_y = range(0, n)
        column_width = 5
        row_format = "|" + ("{:>" + str(column_width) + "}|") * (n + 1)

        title = row_format.format("\\", *titles_x)
        width_table = len(title)
        horiz_sep = "-" * width_table

        res  = horiz_sep + '\n'
        res += title     + '\n'
        res += horiz_sep + '\n'

        for i in range(0, n):
            frm = []
            for x in self.__dd_array[i]:
                if x != "":
                    frm.append("%.2f" % x)
                else:
                    frm.append("")

            res += row_format.format(titles_y[i], *frm) + '\n'

        res += horiz_sep

        return res

    def __fill_table(self):
        n = len(self.xs)
        for k in range(0, n):
            for i in range(0, n):
                for j in range(i, n):
                    if j - i == k:
                        self.__dd_array[i][j] = self.div_diff(i, j)

    def div_diff(self, i, j):
        if i > j:
            print "Error :("
            return 0

        if self.__dd_array[i][j] == "":
            return self.dd_func(i, j)
        else:
            return self.__dd_array[i][j]

    def dd_func(self, i, j):
        if i == j:
            return self.ys[i]
        else:
            return (self.div_diff(i + 1, j) - self.div_diff(i, j - 1)) / (self.xs[j] - self.xs[i])
