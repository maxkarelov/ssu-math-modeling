import sys
import math
import helper

eps = 1e-18

v = 4
a = -math.pi
b =  math.pi
n = 12

if __name__ == "__main__":
    if len(sys.argv) == 2:
        n = int(sys.argv[1]) - 1
    elif len(sys.argv) == 4:
        a = float(sys.argv[1])
        b = float(sys.argv[2])
        n = int(sys.argv[3]) - 1
    elif len(sys.argv) != 1:
        print "Too many or too few args!"
        exit(0)

xs = []
sums = []
ns = []

x = a
step = math.fabs(a - b) / n

while x <= b:
    xs.append(x)
    x += step

def taylor_sin(v, xs):
    sums = []

    for x in xs:
        summand = v * x
        sum = summand
        i = 3
        j = 0
        while abs(summand) > eps:
            summand *= -(v * x) ** 2 / (i * (i - 1))
            sum += summand
            i += 2
            j += 1
        sums.append(round(sum, 4))
        ns.append(j);

    return sums

sums = taylor_sin(v, xs)

#print "Range: {}\nNumber of tests: {}\nV = {}".format([a, b], len(xs), v)
#titles = ["x", "f(x)", "n"]
#data = [xs, sums, ns]
#helper.print_vertical_table(titles, data, 8, 1)