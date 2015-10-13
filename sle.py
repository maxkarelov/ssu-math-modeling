from helper import *

def gauss(A, B):
    n = len(A)

    A.append(B)
    data = rotate_2D_list(A)
    x = [1.0 for i in range(n)] # will be edited and returned

    # Finding an elementary matrix
    for i in range(n):
        k0 = data[i][i]
        lst = data[i]

        for j in range(i + 1, n):
            k1 = data[j][i]
            data[j] = map(lambda a, b: a * -k1 / k0 + b, lst, data[j])

    # Finding an answer
    for i in range(n - 1, -1, -1):

        for j in range(i + 1, n):
            data[i][n] -= data[i][j] * x[j]
            data[i][j] = 0

        x[i] = data[i][n] / data[i][i] 

    return x

v = 4
e = 1.0e-2

A = [[(v +  0)	  , (v +  0) * e, (v +  0) * e, (v +  0) * e, (v +  0) * e, (v +  0) * e],
	 [(v +  2) * e, (v +  2)	, (v +  2) * e, (v +  2) * e, (v +  2) * e, (v +  2) * e],
	 [(v +  4) * e, (v +  4) * e, (v +  4)	  , (v +  4) * e, (v +  4) * e, (v +  4) * e],
	 [(v +  6) * e, (v +  6) * e, (v +  6) * e, (v +  6)    , (v +  6) * e, (v +  6) * e],
	 [(v +  8) * e, (v +  8) * e, (v +  8) * e, (v +  8) * e, (v +  8)    , (v +  8) * e],
	 [(v + 10) * e, (v + 10) * e, (v + 10) * e, (v + 10) * e, (v + 10) * e, (v + 10)]]

B = [v, v + 2, v + 4, v + 6, v + 8, v + 10]

ttl = [x for x in range(len(A))]

#A = [[5.0, 2.0], [2.0, 1.0]]
#B = [7.0, 9.0]
#ttl = [0, 1]

print_table(ttl, ttl, A)
print_table(['B'], [x for x in range(len(B))], rotate_2D_list([B]))
ans = gauss(A, B)
print_table(['X'], [x for x in range(len(ans))], rotate_2D_list([ans]), 18)
