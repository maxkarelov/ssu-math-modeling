import sys
import math
import helper


########################################
## Defining the calculation algorithm ##
########################################

eps = 1e-18
v = 4

# Only for sin(v*x) series
def taylor4sin(xs, ns):
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



#######################################
##       Program starts here         ##
#######################################

if __name__ == "__main__":
    a = 0
    b = 10
    n = 20

    fl_w2f = "write2file" in sys.argv
    fl_pri = "print"      in sys.argv
    fl_dfl = "default"    in sys.argv

    xs = []
    sums = []
    ns = []

    x = a
    step = math.fabs(a - b) / n

    while x <= b:
        xs.append(x)
        x += step

    sums = taylor4sin(xs, ns)

    if fl_dfl: 
        print "Default values:\n[a, b] = {}\nn = {}\nV = {}\neps = {}" \
                .format([a, b], n, v, eps)

    if fl_w2f:
        file = open("values.txt", 'w') 
        file.write(str(xs) + '\n')
        file.write(str(sums))
        file.close()

        print "Lists were written into \"values.txt\""

    if fl_pri:
        print "Range: {}\nNumber of tests: {}\nV = {}" \
                .format([a, b], len(xs), v)

        titles = ["x", "f(x)", "n"]
        data = [xs, sums, ns]
        helper.print_table(data=helper.rotate_2D_list(data), titles_x=titles, \
                           column_width=10, vert_sep=True, horiz_sep=True)