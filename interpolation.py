import sys
import ast
import math

import matplotlib.pyplot as plt

from helper import *
from taylor_sin import taylor_sin

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
    x_n = 0
    for i in range(1, len(xs)):
        if xs[i - 1] <= x < xs[i]:
            x_n = i
            break

    s = CubicSpline(xs, ys).splines[x_n]
    dx = x - s.x
    return s.a + (s.b + (s.c / 2.0 + s.d * dx / 6.0) * dx) * dx

# Main lists
xs = []
ys = []

# Reading running args
form = "lagrange"
if __name__ == "__main__":
    if len(sys.argv) == 2:
        form = str(sys.argv[1])
    elif len(sys.argv) != 1:
        print "Too many or too few args!"
        exit(0)

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
elif form == "div_diff":
    print DividedDiffirence(xs, ys)
    exit(0)
else:
    print "I don't know this type of interpolation :("
    exit(0)

# Calculating
step = 0.01 #abs(xs[0] - xs[1]) / 16.0
for x in frange(xs[0], xs[size - 1], step):
    xs_new.append(x)
    ys_new.append(f(x, xs, ys))

#sinys = taylor_sin(4, xs_new)
#errys = [sinys[i] - ys_new[i] for i in range(0, len(sinys))]

#for i in range(0, len(sinys)):
#    print "x = {}, error = {}".format(xs_new[i], errys[i])

#for x in xs_old:
#    plt.plot([x, x], [-100, 100])

# Plot drawing
plt.plot(xs_old, ys_old)
plt.plot(xs_new, ys_new)
#plt.plot(xs_new, errys)
plt.axis(range(-2, 2))
plt.show()