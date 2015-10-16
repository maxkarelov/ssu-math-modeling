from helper import *

def normalize_list(lst, key=0):
    return map(lambda x: x / float(lst[key]), lst)

def get_identity_matrix(size):
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

def inverse_2D_list(data):
    return [l[::-1] for l in data][::-1]

def triangular(matrix):
    n = len(matrix)

    # Finding the elementary matrix
    for i in range(n):
        matrix[i:] = sorted(matrix[i:], key=lambda x: abs(x[i]), reverse=True)
        
        k0 = matrix[i][i]

        for j in range(i + 1, n):
            k1 = matrix[j][i]
            matrix[j] = map(lambda a, b: a * -k1 / k0 + b, matrix[i], matrix[j])

    return matrix

def sle_gauss(A, B):
    n = len(A)

    data = [A[i] + [B[i]] for i in range(n)]
    x = range(n) # will be edited and returned

    # Finding the triangular matrix
    data = triangular(matrix=data)

    # Finding the answer
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
    
    data = map(lambda a, b: a + b, inverse_2D_list(l1), inverse_2D_list(l2))
    data = triangular(data)

    return inverse_2D_list([l[n:] for l in data])

def determinant(matrix):
    trng = triangular(matrix)
    return reduce(lambda a, b: a * b, [trng[i][i] for i in range(len(trng))])

v = 4.0
e = 1.0e-2

A = [[(v +  0)	  , (v +  0) * e, (v +  0) * e, (v +  0) * e, (v +  0) * e, (v +  0) * e],
	 [(v +  2) * e, (v +  2)	, (v +  2) * e, (v +  2) * e, (v +  2) * e, (v +  2) * e],
	 [(v +  4) * e, (v +  4) * e, (v +  4)	  , (v +  4) * e, (v +  4) * e, (v +  4) * e],
	 [(v +  6) * e, (v +  6) * e, (v +  6) * e, (v +  6)    , (v +  6) * e, (v +  6) * e],
	 [(v +  8) * e, (v +  8) * e, (v +  8) * e, (v +  8) * e, (v +  8)    , (v +  8) * e],
	 [(v + 10) * e, (v + 10) * e, (v + 10) * e, (v + 10) * e, (v + 10) * e, (v + 10)]]

B = [18, 38.88, 67.68, 104.4, 149.04, 201.6]

ttl = [x for x in range(len(A))]
ans = sle_gauss(A, B)

print "Matrix:"
print_table(titles_x=ttl,   titles_y=ttl, data=A)

print "Inverse matrix:"
print_table(titles_x=ttl,   titles_y=ttl, data=inverse_matrix(A), column_width=10, rnd=5)

print "Determinant of it: ", determinant(A)

print "Column B:"
print_table(titles_x=['B'], titles_y=[x for x in range(len(B))],   data=rotate_2D_list([B]), column_width=7)

print "Found column X:"
print_table(titles_x=['X'], titles_y=[x for x in range(len(ans))], data=rotate_2D_list([ans]), column_width=7, rnd=5)