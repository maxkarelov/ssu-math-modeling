import sys
import math

import sle

from helper import *

########################################################################
## Defining functions for solving the systems of non-linear equations ##
########################################################################

# Simple iterations
def simple_iter(equations, initial_x, eps=1e-6):
    xs = [initial_x]
    delta = eps * 10

    while delta > eps:
        x_n = xs[len(xs) - 1]
        x_n1 = [e(*x_n) for e in equations]
        delta = max([abs(x_n[i] - x_n1[i]) for i in range(len(x_n1))])
        xs.append(x_n1)

    return xs[len(xs) - 1]

# Newton's algorithm
def newton(equations, initial_x, eps=1e-6):
    xs = [initial_x]
    delta = eps * 10

    while delta > eps:
        x_n = xs[len(xs) - 1]
        yacobi_matrix = [[derivative(f, x_n, key=i) 
                            for i in range(len(initial_x))]  
                         for f in equations]

        F = [-f(*x_n) for f in equations]
        delta_xs = sle.gauss(A=yacobi_matrix, B=F)
        x_n1 = [x_n[i] + delta_xs[i] for i in range(len(x_n))]
        xs.append(x_n1)
        delta = max([abs(x_n1[i] - x_n[i]) for i in range(len(x_n))])

    return xs[len(xs) - 1]


if __name__ == "__main__":

    equations = [
        lambda x, y: 0.1 * x ** 2 + x + 0.2 * y ** 2 - 0.3, 
        lambda x, y: 0.2 * x ** 2 + y - 0.1 * x * y - 0.7
    ]

    initial_x = [
        0.25,
        0.75
    ]

    print "Data:"
    print '''
    equations = [
        lambda x, y: 0.1 * x ** 2 + x + 0.2 * y ** 2 - 0.3, 
        lambda x, y: 0.2 * x ** 2 + y - 0.1 * x * y - 0.7
    ]

    initial_x = [
        0.25,
        0.75
    ]
    '''

    ans = 0
    if "newton" in sys.argv:
        ans = newton(equations, initial_x)
    elif "iteration" in sys.argv: 
        ans = simple_iter(equations, initial_x)
    else:
        print "Undefined method called"
        exit(0)

    if ans != 0:
        print "Answer:"
        print_table(data=rotate_2D_list([ans]), titles_y=['x', 'y'], 
                    column_width=18, vert_sep=True, horiz_sep=True)
        print