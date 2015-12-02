from collections import defaultdict
import math

def normalize_list(lst, key=0):
    return map(lambda x: x / float(lst[key]), lst)

def get_identity_matrix(size):
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

def reverse_2D_list(data):
    return [l[::-1] for l in data][::-1]

def rotate_2D_list(data):
    data_new = []
    for i in xrange(len(data[0])):
        s = []
        for x in data:
            s.append(x[i])
        data_new.append(s)

    return data_new

def round_list(data, k):
    if not isinstance(data[0], list):
        return [round(x, k) for x in data]
    else:
        data_new = []
        for l in data:
            data_new.append(round_list(l, k))

        return data_new

def derivative(f, x0, key=0, delta=1e-9):
    if not isinstance(x0, list): x0 = [x0]
    ld = x0[:key] + [x0[key] + delta] + x0[key + 1:]
    return (f(*ld) - f(*x0)) / delta

def print_table(data, titles_x=[], titles_y=[], column_width=5, rnd=0, \
                horiz_sep=False, vert_sep=False):

    nx = len(data[0])
    ny = len(data)

    ttl_x_fl = len(titles_x) > 0
    ttl_y_fl = len(titles_y) > 0

    if rnd > 0:
        data = round_list(data, rnd)

    if vert_sep:
        row_format = "|" + ("{:>" + str(column_width) + "}|") * (nx + ttl_y_fl)
    else:
        row_format = ("{:>" + str(column_width) + "}") * (nx + ttl_y_fl)

    table_width = (column_width + vert_sep) * (nx + ttl_y_fl) + vert_sep

    horiz = "-" * table_width

    if ttl_x_fl:
        if ttl_y_fl:
            title = row_format.format("", *titles_x)
        else:
            title = row_format.format(*titles_x)

        if horiz_sep: print horiz
        print title

    if horiz_sep: print horiz

    for i in range(0, ny):
        if ttl_y_fl:
            print row_format. \
                    format(titles_y[i] if ttl_y_fl else None, *data[i])
        else:
            print row_format.format(*data[i])

    if horiz_sep: print horiz

def frange(x, y, jump):
    while x < y:
      yield x
      x += jump


class Dot:
    def __init__(self, x, y): self.x, self.y = [x, y]


class Tuple: a, b, c, d, x = [0.0, 0.0, 0.0, 0.0, 0.0]