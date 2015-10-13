import sys
import ast
import math
import bisect

import matplotlib.pyplot as plt

from helper import *
from taylor_sin import taylor4sin

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

            
cs = 0
def CubSpl(x, xs, ys):
    distribution = sorted([t[1].x for t in cs.splines.items()])
    indx = bisect.bisect_left(distribution, x)
    if indx == len(distribution): return 0
    dx = x - cs.splines[indx].x
    return cs.splines[indx].a + cs.splines[indx].b * dx + cs.splines[indx].c * dx ** 2 / 2. + cs.splines[indx].d * dx ** 3 / 6.0

# Main lists
xs = []
ys = []

step = 0.01
fl_dd = 0
fl_graph = 0
fl_print = 0

# Reading running args
form = "lagrange"
if __name__ == "__main__":
    if "lagrange".lower() in sys.argv: form = "lagrange"
    if "newton".lower()   in sys.argv: form = "newton"
    if "spline".lower()   in sys.argv: form = "spline"

    if "div_diff".lower() in sys.argv: fl_dd  = 1

    if "print".lower() in sys.argv: fl_print = 1
    if "plot".lower()  in sys.argv: fl_graph = 1

#    print "Use default step ({})? (y/n)".format(step)
#    dv = sys.stdin.read(1)
#
#    print "-" * 30
#
#    if dv.lower() == "n":
#        step = raw_input("a = {}\n".format(a))
#
#        step = float(step)

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
elif form == "spline"  : 
    f = CubSpl
    cs = CubicSpline(xs, ys)
else:
    print "I don't know this type of interpolation :("
    exit(0)

# Calculating
for x in frange(xs[0], xs[size - 1], step):
    xs_new.append(x)
    ys_new.append(f(x, xs, ys))

sinys = taylor4sin(xs_new)
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