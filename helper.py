from collections import defaultdict
import math

def rotate_2D_list(data):
    data_new = []
    for i in xrange(len(data[0])):
        s = []
        for x in data:
            s.append(x[i])
        data_new.append(s)

    return data_new

def round_list(data, k):
    if not isinstance(data[0], list):
        return [round(x, k) for x in data]
    else:
        data_new = []
        for l in data:
            data_new.append(round_list(l, k))

        return data_new

def print_vertical_table(titles, data, column_width=30):
    row_format = "|" + ("{:>" + str(column_width) + "}|") * len(data)

    # Reorganize data array
    data_new = rotate_2D_list(data)

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

def print_table(titles_x, titles_y, data, column_width=5, rnd=0):
    nx = len(data[0])
    ny = len(data)

    if rnd > 0:
        data = round_list(data, rnd)

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
                if i + k < n:
                    self.__dd_array[i][i + k] = self.div_diff(i, i + k)

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


class Tuple: a, b, c, d, x = [0.0, 0.0, 0.0, 0.0, 0.0]


class CubicSpline:
    
    class Dot:
        def __init__(self, x, y): self.x, self.y = [x, y]

    splines = defaultdict(lambda: Tuple())

    def __init__(self, xs, ys):
        dots = [self.Dot(xs[i], ys[i]) for i in range(len(xs))]

        for i in range(len(dots)): self.splines[i].x, self.splines[i].a = dots[i].x, dots[i].y

        in_step = dots[1].x - dots[0].x

        alpha, beta = [defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)]

        for i in range(1, len(dots) - 1):
            C = 4.0 * in_step
            F = 6.0 * ((dots[i + 1].y - dots[i].y) / in_step - (dots[i].y - dots[i - 1].y) / in_step)
            z = (in_step * alpha[i - 1] + C)
            alpha[i] = -in_step / z
            beta[i] = (F - in_step * beta[i - 1]) / z

        for i in reversed(range(1, len(dots) - 1)): self.splines[i].c = alpha[i] * self.splines[i + 1].c + beta[i]

        for i in reversed(range(1, len(dots))):
            hi = dots[i].x - dots[i - 1].x
            self.splines[i].d = (self.splines[i].c - self.splines[i - 1].c) / hi
            self.splines[i].b = hi * (2.0 * self.splines[i].c + self.splines[i - 1].c) / 6.0 + (dots[i].y - dots[i-  1].y) / hi


def gauss(A, B):
    n = len(A)

    A.append(B)
    data = rotate_2D_list(A)
    x = [1.0 for i in range(n)] # will be edited and returned

    # Finding an elementary matrix
    for i in range(n):
        k0 = data[i][i]
        lst = data[i]

        for j in range(i + 1, n):
            k1 = data[j][i]
            data[j] = map(lambda a, b: a * -k1 / k0 + b, lst, data[j])

    # Finding an answer
    for i in range(n - 1, -1, -1):

        for j in range(i + 1, n):
            data[i][n] -= data[i][j] * x[j]
            data[i][j] = 0

        x[i] = data[i][n] / data[i][i] 

    return x