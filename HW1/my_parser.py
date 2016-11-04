class Operation:
    def to_string(self):
        return '(' + self.left.to_string() + self.sym + self.right.to_string() + ')'

    def is_equal(self, exp2):
        return self.hash == exp2.hash
        # return self.sym == exp2.sym and self.left.is_equal(exp2.left) and self.right.is_equal(exp2.right)


class Var:
    sym = ''

    def __init__(self, name):
        self.name = name
        self.hash = hash(name) % mod

    def to_string(self):
        return self.name

    def is_equal(self, exp2):
        return self.hash == exp2.hash
        # return self.sym == exp2.sym and self.name == exp2.name


class Neg:
    sym = '!'
    num = 13

    def __init__(self, var):
        self.var = var
        self.hash = self.var.hash * self.num % mod

    def to_string(self):
        return self.sym + self.var.to_string()

    def is_equal(self, exp2):
        return self.hash == exp2.hash
        # return self.sym == exp2.sym and self.var.is_equal(exp2.var)


class Conj(Operation):
    sym = '&'
    num = 17

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hash = (self.left.hash * self.num + self.right.hash * self.num ** 2) % mod


class Disj(Operation):
    sym = '|'
    num = 19

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hash = (self.left.hash * self.num + self.right.hash * self.num ** 2) % mod


class Exp(Operation):
    sym = '->'
    num = 23

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hash = (self.left.hash * self.num + self.right.hash * self.num ** 2) % mod


def parse_conj():
    global line, cur
    e = parse_neg()
    while cur < len(line) and line[cur] == '&':
        cur += 1
        e = Conj(e, parse_neg())
    return e


def parse_disj():
    global line, cur
    e = parse_conj()
    while cur < len(line) and line[cur] == '|':
        cur += 1
        e = Disj(e, parse_conj())
    return e


def parse_exp():
    global line, cur
    e = parse_disj()
    if cur < len(line) and line[cur] == '-':
        cur += 2
        e = Exp(e, parse_exp())
    return e


def parse_neg():
    global line, cur
    if line[cur] == '!':
        cur += 1
        e = parse_neg()
        return Neg(e)
    elif line[cur] == '(':
        cur += 1
        e = parse_exp()
        assert (line[cur] == ')')
        cur += 1
        return e
    else:
        cur_old = cur
        while cur < len(line) and ('A' <= line[cur] <= 'Z' or '0' <= line[cur] <= '9'):
            cur += 1
        return Var(line[cur_old:cur])


def line_from_file(line1):
    global line, cur
    cur = 0
    line = line1


# cur = 0
# line = input()
# print(parse_exp().to_string())
mod = 10 ** 9 + 7
