import sys

from helper import *


##################################################
## Defining functions for working with matrices ##
##################################################

def triangular(matrix):
    n = len(matrix)

    # Finding the elementary matrix
    for i in range(n):
        matrix[i:] = sorted(matrix[i:], key=lambda x: abs(x[i]), reverse=True)
        
        k0 = matrix[i][i]

        for j in range(i + 1, n):
            k1 = matrix[j][i]
            matrix[j] = map(lambda a, b: a * -k1 / k0 + b, \
                            matrix[i], matrix[j])

    return matrix

def sle_gauss(A, B):
    n = len(A)

    data = [A[i] + [B[i]] for i in range(n)]
    x = range(n) # will be edited and returned

    data = triangular(matrix=data)

    for i in range(n - 1, -1, -1):

        for j in range(i + 1, n):
            data[i][n] -= data[i][j] * x[j]
            data[i][j] = 0

        x[i] = data[i][n] / data[i][i] 

    return x

def inverse_matrix(matrix):
    n = len(matrix)

    identity = get_identity_matrix(n)

    data = map(lambda a, b: a + b, matrix, identity)
    ttl = range(n)

    data = triangular(data)
    data = [normalize_list(data[i], key=i) for i in range(n)]

    # list[::-1] means reversing of the list

    l1 = [l[:n] for l in data]
    l2 = [l[n:] for l in data]
    
    data = map(lambda a, b: a + b, reverse_2D_list(l1), reverse_2D_list(l2))
    data = triangular(data)

    return reverse_2D_list([l[n:] for l in data])

def determinant(matrix):
    trng = triangular(matrix)
    return reduce(lambda a, b: a * b, [trng[i][i] for i in range(len(trng))])



#######################################
##       Program starts here         ##
#######################################

if __name__ == "__main__":
    v = 4.0
    e = 1.0e-2
    lv = [v, v + 2, v + 4, v + 6, v + 8, v + 10]
    le = map(lambda x: x * e, lv)

    A = [[lv[i] if i == j else le[i] for j in range(6)] for i in range(6)]
    B = [18, 38.88, 67.68, 104.4, 149.04, 201.6]

    ans = sle_gauss(A, B)

    print "Matrix:"
    print_table(data=A, horiz_sep=True, vert_sep=True)
    print

    print "Column B:"
    print_table(data=rotate_2D_list([B]), horiz_sep=True, vert_sep=True, \
                column_width=7)
    print

    if "inverse" in sys.argv:
        print "Inverse matrix:"
        print_table(data=inverse_matrix(A), horiz_sep=True, vert_sep=True, \
                    column_width=12, rnd=6)
        print

    if "determinant" in sys.argv:
        print "Determinant of it: ", determinant(A)
        print

    if "sle" in sys.argv:
        print "Found column X:"
        print_table(data=rotate_2D_list([ans]), horiz_sep=True, \
                    vert_sep=True, column_width=7, rnd=5)