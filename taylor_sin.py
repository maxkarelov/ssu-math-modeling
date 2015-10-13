import sys
import math
import helper

eps = 1e-18
v = 4

def taylor4sin(xs):
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

a = 0
b = 10
n = 20

fl_w2f = 0
fl_pri = 0
fl_dfl = 0

if __name__ == "__main__":

#    print "Use default values? (y/n)"
#    dv = sys.stdin.read(1)
#
#    print "-" * 30
#
#    if dv.lower() == "n":
#        a = raw_input("a = {}\n".format(a))
#        b = raw_input("b = {}\n".format(b))
#        n = raw_input("n = {}\n".format(n))
#
#        a = float(a)
#        b = float(b)
#        n = int(n)

    argsize = len(sys.argv)

    if "write2file" in sys.argv: fl_w2f = 1
    if "print"      in sys.argv: fl_pri = 1
    if "default"    in sys.argv: fl_dfl = 1
        
xs = []
sums = []
ns = []

x = a
step = math.fabs(a - b) / n

while x <= b:
    xs.append(x)
    x += step

if __name__ == "__main__":

    sums = taylor4sin(xs)

    if fl_dfl: print "Default values:\n[a, b] = {}\nn = {}\nV = {}\neps = {}".format([a, b], n, v, eps)

    if fl_w2f:
        file = open("values.txt", 'w') 
        file.write(str(xs) + '\n')
        file.write(str(sums))
        file.close()

        print "Lists were written into \"values.txt\""

    if fl_pri:
        print "Range: {}\nNumber of tests: {}\nV = {}".format([a, b], len(xs), v)
        titles = ["x", "f(x)", "n"]
        data = [xs, sums, ns]
        helper.print_vertical_table(titles, data, 20)