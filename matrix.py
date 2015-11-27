import sys

from numpy import *

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


###################################################################
## Defining funcions for solving the systems of linear equations ##
###################################################################

# Tridiagonal matrix algorithm
def tridiagonal(A, B):
    n = len(A)

    data = [A[i] + [B[i]] for i in range(n)]

    # Start data
    x = [0] * n
    P = [0] * n
    Q = [0] * n
    alpha = [0] + [data[i + 1][i] for i in range(n - 1)]
    beta  = [-data[i][i] for i in range(n)]
    gamma = [data[i][i + 1] for i in range(n)]
    delta = B

    # Direct steps
    P[0] =  gamma[0] / beta[0]
    Q[0] = -delta[0] / beta[0]

    for i in range(1, n):
        P[i] = gamma[i] / (beta[i] - alpha[i] * P[i - 1])
        Q[i] = (alpha[i] * Q[i - 1] - delta[i]) / \
               (beta[i] - alpha[i] * P[i - 1])

    # Reverse steps
    x[n - 1] = (alpha[n - 1] * Q[n - 2] - delta[n - 1]) / \
               (beta[n - 1] - alpha[n - 1] * P[n - 2])

    for i in range(n - 2, -1, -1):
        x[i] = P[i] * x[i + 1] + Q[i]

    return x    

# Gauss' algorithm
def gauss(A, B):
    n = len(A)

    data = [A[i] + [B[i]] for i in range(n)]
    x = range(n) # will be edited and returned

    data = triangular(data)

    for i in range(n - 1, -1, -1):

        for j in range(i + 1, n):
            data[i][n] -= data[i][j] * x[j]
            data[i][j] = 0

        x[i] = data[i][n] / data[i][i] 

    return x

# Yacobi's algorithm
def yacobi(A, B, eps=1.0e-4):

    def yacobi_iter(X, k):
        n = len(A)

        # Uncomment line below for the checking variable k
        # print k

        Xnew = range(n)
        need_for_new_iteration = False

        for i in range(n):
            s = 0

            for j in range(n):
                if i != j:
                    s += A[i][j] * X[j]

            Xnew[i] = 1 / A[i][i] * (B[i] - s)

            if abs(Xnew[i] - X[i]) > eps:
                need_for_new_iteration = True

        if need_for_new_iteration:
            return yacobi_iter(Xnew, k + 1)
        else:
            return Xnew

    X = [B[i] / A[i][i] for i in range(len(A))]

    return yacobi_iter(X, 0)

# Seidel-Gauss algo
def seidel(A, B, eps=1.0e-4):

    def seidel_iter(X, k):
        n = len(A)

        # Uncomment line below for the checking variable k
        # print k

        Xnew = range(n)
        need_for_new_iteration = False

        for i in range(n):
            s1 = s2 = 0

            for j in range(n):
                if j < i:
                    s1 += A[i][j] * Xnew[j]
                elif j > i:
                    s2 += A[i][j] * X[j]

            Xnew[i] = 1 / A[i][i] * (B[i] - s1 - s2)

            if abs(Xnew[i] - X[i]) > eps:
                need_for_new_iteration = True

        if need_for_new_iteration:
            return seidel_iter(Xnew, k + 1)
        else:
            return Xnew

    X = [B[i] / A[i][i] for i in range(len(A))]

    return seidel_iter(X, 0)

# Conjugate gradient method
def cg(A, B, eps=1.0e-12):
    n = len(A)

    A = array(A)
    b = array(B)

    x = [[B[i] / A[i][i] for i in range(len(A))]]
    ksi = [b - dot(A, x[0])]
    p = [ksi[0]]
    q = []
    alpha = []
    beta = []

    k = 0

    while True:
        q.append(dot(A, p[k]))
        alpha.append((ksi[k] * p[k]) / (q[k] * p[k]))
        x.append(x[k] + alpha[k] * p[k])
        ksi.append(ksi[k] - alpha[k] * q[k])

        if linalg.norm(ksi[k + 1]) <= eps:
            return x[k + 1]

        beta.append((ksi[k + 1] * q[k]) / (p[k] * q[k]))
        p.append(ksi[k + 1] - beta[k] * p[k])

        k += 1


#######################################################################
## Defining funcions for solving the systems of non-linear equations ##
#######################################################################




#######################################
##       Program starts here         ##
#######################################

if __name__ == "__main__":
    v = 4.0
    e = 1.0e-2

    n = 10
    lv = [v + i for i in range(0, n * 2, 2)]
    le = map(lambda x: x * e, lv)

    A = [[lv[i] if i == j else le[i] for j in range(n)] for i in range(n)]

    # For tridiagonal matrix algorithm
    if "tridiagonal" in sys.argv: 
        for i in range(len(A)):
           for j in range(len(A)):
              if abs(i - j) > 1:
                  A[i][j] = 0
                  
    B = dot(array(A), lv)

    print "Matrix:"
    print_table(data=A, horiz_sep=True, vert_sep=True)
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
        if "gauss" in sys.argv:
            ans = gauss(A, B)
        elif "yacobi" in sys.argv:
            ans = yacobi(A, B)
        elif "seidel" in sys.argv:
            ans = seidel(A, B)
        elif "tridiagonal" in sys.argv: 
            ans = tridiagonal(A, B)
        elif "cg" in sys.argv: 
            ans = cg(A, B)
        else:
            print "Sorry, I don't know this algorithm"
            exit(0)

        print "Column B:"
        print_table(data=rotate_2D_list([B]), horiz_sep=True, vert_sep=True, \
                    column_width=7)
        print

        print "Found column X:"
        print_table(data=rotate_2D_list([ans]), horiz_sep=True, \
                    vert_sep=True, column_width=16)
        print
        