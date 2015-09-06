import sys
import math
import helper

eps = 1e-9

v = 4

a = 0
b = 10
n = 10

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

for x in xs:
	summand = v * x
	sum = summand
	i = 3
	n = 0
	while math.fabs(summand) > eps:
		summand *= -(v * x) ** 2 / (i * (i - 1))
		sum += summand
		i += 2
		n += 1
	sums.append(round(sum, 4))
	ns.append(n);

print "Range: {}\nNumber of tests: {}\nV = {}".format([a, b], len(xs), v)

titles = ["x", "f(x)", "n"]
data = [xs, sums, ns]
helper.print_table(titles, data, 8)