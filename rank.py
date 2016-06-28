class ArrayView(object):

    def __init__(self, data, offset, length):
        self.data = data
        self.offset = offset
        self.length = length

    def subview(self, n, blocks):
        return ArrayView(self.data, self.offset+(self.length/blocks)*n, self.length/blocks)

    def __getitem__(self, index):
        assert 0 <= index < self.length
        return self.data[self.offset+index]

    def __setitem__(self, index, value):
        assert 0 <= index < self.length
        self.data[self.offset+index] = value


class Array(object):

    def __init__(self, shape, data):
        self.shape = shape
        self.data = data

    def view(self):
        return ArrayView(self.data, 0, len(self.data))

    def __eq__(self, other):
        return (self.shape == other.shape) and (self.data == other.data)


class Sum(object):

    def get_shape(self, sy):
        return sy[:-1]

    def interp(self, sy, vy, vz):
        p = product(sy[:-1])
        for i in xrange(p):
            vz[i] = 0

        for i in xrange(sy[-1]):
            vyi = vy.subview(i, sy[-1])
            for j in xrange(p):
                vz[j] += vyi[j]


def product(l):
    x = 1
    for e in l:
        x *= e
    return x


def interp_monad(op, ry, y):
    if ry is None:
        ry = len(y.shape)

    shape = op.get_shape(y.shape[:ry]) + y.shape[ry:]
    z = Array(shape, [0.0 for _ in xrange(product(shape))])

    vy = y.view()
    vz = z.view()

    p = product(y.shape[ry:])
    for i in xrange(p):
        op.interp(y.shape[:ry], vy.subview(i,p), vz.subview(i,p))

    return z


assert interp_monad(Sum(), 1, Array((2,),[1,2])) == Array((),[3])