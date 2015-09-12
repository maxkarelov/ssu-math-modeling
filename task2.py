import helper
import sys
import ast
import matplotlib.pyplot as plt

def Lnk(x, xs, ys) :
	size = len(xs)
	lagrange = 0
	basic = 1

	for i in range(0, size - 1) :
		basic = 1

		for j in range(0, size - 1) :
			if i != j :
				basic *= (x - xs[j]) / (xs[i] - xs[j])

		lagrange += basic * ys[i]

	return lagrange

# Main lists
xs = []
ys = []

# Reading running args
n = 1
if __name__ == "__main__" :
	if len(sys.argv) == 2 :
		n = int(sys.argv[1])
	elif len(sys.argv) != 1 :
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

for i in range(0, n) :
	for x in helper.frange(xs[0], xs[size - 1], 0.1) :
		xs_new.append(x)
		ys_new.append(Lnk(x, xs, ys))

plt.plot(xs, ys)
plt.plot(xs_new, ys_new)
plt.axis(range(-2, 2))
plt.show()