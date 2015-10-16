import sys
import ast
import math
import bisect

import matplotlib.pyplot as plt

from helper import *
from taylor import taylor4sin


#############################################################
## Defining the class which used in Newton's interpolation ##
#############################################################

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
            return (self.div_diff(i + 1, j) - self.div_diff(i, j - 1)) / \
                    (self.xs[j] - self.xs[i])


#######################################
## Defining interpolation algorithms ##
#######################################

# Lagrange form
def Lnk(x, xs, ys):
    size = len(xs)
    lagrange = 0

    for i in range(0, size - 1):
        basic = 1

        for j in range(0, size - 1):
            if i != j:
                basic *= (x - xs[j]) / (xs[i] - xs[j])

        lagrange += basic * ys[i]

    return lagrange

# Newton form
def Pn(x, xs, ys):
    dd = DividedDiffirence(xs, ys)
    div_diff = dd.div_diff

    n = len(xs)
    newton = ys[0]

    for i in range(1, n):
        basic = div_diff(0, i)

        for j in range(0, i):
            basic *= (x - xs[j])

        newton += basic

    return newton

# Cubic splines            
def CubSpl(x, xs, ys):
    splines = defaultdict(lambda: Tuple())

    dots = [Dot(xs[i], ys[i]) for i in range(len(xs))]

    for i in range(len(dots)): 
        splines[i].x, splines[i].a = dots[i].x, dots[i].y

    in_step = dots[1].x - dots[0].x

    alpha, beta = [defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)]

    for i in range(1, len(dots) - 1):
        C = 4.0 * in_step
        F = 6.0 * ((dots[i + 1].y - dots[i].y) / in_step - \
            (dots[i].y - dots[i - 1].y) / in_step)
        z = (in_step * alpha[i - 1] + C)

        alpha[i] = -in_step / z
        beta[i] = (F - in_step * beta[i - 1]) / z

    for i in reversed(range(1, len(dots) - 1)): 
        splines[i].c = alpha[i] * splines[i + 1].c + beta[i]

    for i in reversed(range(1, len(dots))):
        hi = dots[i].x - dots[i - 1].x
        splines[i].d = (splines[i].c - splines[i - 1].c) / hi
        splines[i].b = hi * (2.0 * splines[i].c + \
            splines[i - 1].c) / 6.0 + (dots[i].y - dots[i - 1].y) / hi

    distribution = sorted([t[1].x for t in splines.items()])
    indx = bisect.bisect_left(distribution, x)
    if indx == len(distribution): return 0
    dx = x - splines[indx].x
    return splines[indx].a + splines[indx].b * dx + \
        splines[indx].c * dx ** 2 / 2.0 + splines[indx].d * dx ** 3 / 6.0



#######################################
##       Program starts here         ##
#######################################

if __name__ == "__main__":

    # Main lists
    xs = []
    ys = []

    step = 0.01
    fl_dd = False
    fl_graph = False
    fl_print = False

    # Reading running args
    form = "lagrange"

    if "lagrange".lower() in sys.argv: form = "lagrange"
    if "newton".lower()   in sys.argv: form = "newton"
    if "spline".lower()   in sys.argv: form = "spline"

    if "div_diff".lower() in sys.argv: fl_dd  = True

    if "print".lower() in sys.argv: fl_print = True
    if "plot".lower()  in sys.argv: fl_graph = True

    # File reading
    file = open("values.txt", 'r')
    temp = file.read().split('\n')
    xs = ast.literal_eval(temp[0])
    ys = ast.literal_eval(temp[1])
    size = len(xs)
    xs_new = []
    ys_new = []
    xs_old = xs
    ys_old = ys

    # Choosing function
    f = Lnk
    if   form == "lagrange": f = Lnk
    elif form == "newton"  : f = Pn
    elif form == "spline"  : f = CubSpl
    else:
        print "I don't know this type of interpolation :("
        exit(0)

    # Calculating
    for x in frange(xs[0], xs[size - 1], step):
        xs_new.append(x)
        ys_new.append(f(x, xs, ys))

    sinys = taylor4sin(xs=xs_new, ns=[])
    errys = [sinys[i] - ys_new[i] for i in range(0, len(sinys))]

    if fl_print:
        titles = ["Point", "Interpolate", "Expected", "Differece"]
        data = [xs_new, ys_new, sinys, errys]
        print_vertical_table(titles, data, 20)

    if fl_dd:
        print "Divided difference:"
        print DividedDiffirence(xs, ys)

    if fl_graph:
        plt.plot(xs_old, ys_old)
        plt.plot(xs_new, ys_new)
        plt.show()