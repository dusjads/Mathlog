class Operation:
    def to_string(self):
        return '(' + self.left.to_string() + self.sym + self.right.to_string() + ')'

    def is_equal(self, exp2):
        return self.hash == exp2.hash
        # return self.sym == exp2.sym and self.left.is_equal(exp2.left) and self.right.is_equal(exp2.right)


class Unary:
    def is_equal(self, exp2):
        return self.hash == exp2.hash


class Fun(Unary):  # функция -- часть умножаемого
    num = 31

    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.hash = (hash(self.name) * self.num + sum(list(i.hash for i in args)) * self.num ** 2) % mod

    def to_string(self):
        res = self.name + '('
        for i in self.args[:-1]:
            res += i.to_string + ','
        res += self.args[-1].to_string + ')'
        return res


class Summ(Operation):
    sym = '*'
    num = 41

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hash = (self.left.hash * self.num + self.right.hash * self.num ** 2) % mod


class Term(Operation):
    sym = '+'
    num = 43

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hash = (self.left.hash * self.num + self.right.hash * self.num ** 2) % mod


class Pred(Unary):  # предикат
    sym = ''
    num = 47

    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.hash = (hash(self.name) * self.num + sum(list(i.hash for i in args)) * self.num ** 2) % mod

    def to_string(self):
        res = self.name
        if len(self.args) != 0:
            res += '('
            for i in self.args[:-1]:
                res += i.to_string + ','
            res += self.args[-1].to_string() + ')'
        return res


class Var:
    sym = ''

    def __init__(self, name):
        self.name = name
        self.hash = hash(name) % mod

    def to_string(self):
        return self.name

    def is_equal(self, exp2):
        return self.hash == exp2.hash


class Plus_one(Unary):
    sym = "'"
    num = 57

    def __init__(self, args):
        self.args = args
        self.hash = self.args.hash * self.num % mod

    def to_string(self):
        return self.args.to_string() + self.sym


class Unar(Unary):
    sym = '!'
    num = 13

    def __init__(self, args):
        self.args = args
        self.hash = self.args.hash * self.num % mod

    def to_string(self):
        return self.sym + self.args.to_string()


class Quan(Unary):
    num = 61

    def __init__(self, sym, var, args):
        self.sym = sym
        self.var = var
        self.args = args
        self.hash = (self.var.hash * self.num + self.args.hash * self.num ** 2 + ord(self.sym)) % mod

    def to_string(self):
        return '(' + self.sym + self.var.to_string() + self.args.to_string() + ')'


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


class Eq(Operation):
    sym = '='
    num = 53

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hash = (self.left.hash * self.num + self.right.hash * self.num ** 2) % mod


class Nothing(Unary):
    sym = ''
    num = 0

    def __init__(self):
        self.args = None
        self.hash = 0


def parse_term():
    global line, cur
    e = parse_summ()
    while cur < len(line) and line[cur] == '+':
        cur += 1
        e = Term(e, parse_summ())
    return e


def parse_summ():
    global line, cur
    e = parse_mul()
    while cur < len(line) and line[cur] == '*':
        cur += 1
        e = Summ(e, parse_mul())
    return e


def parse_conj():
    global line, cur
    e = parse_unar()
    while cur < len(line) and line[cur] == '&':
        cur += 1
        e = Conj(e, parse_unar())
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
        tmp = parse_exp()
        if tmp is None:
            return None
        e = Exp(e, tmp)
    return e


def parse_unar():
    global line, cur
    if line[cur] == '!':
        cur += 1
        e = parse_unar()
        return Unar(e)
    elif line[cur] == '@' or line[cur] == '?':
        return parse_quan()
    elif line[cur] == '(':
        cur += 1
        old_cur = cur
        e = parse_exp()
        if e is not None:
            assert (line[cur] == ')')
            cur += 1
            return e
        cur = old_cur - 1
    return parse_pred()


def parse_pred():
    global line, cur
    if 'A' <= line[cur] <= 'Z':
        name = ''
        while cur < len(line) and ('A' <= line[cur] <= 'Z' or '0' <= line[cur] <= '9'):
            name += line[cur]
            cur += 1
        args = []

        if cur < len(line) and line[cur] == '(':
            while line[cur] != ')':
                cur += 1
                args.append(parse_term())
            cur += 1
        return Pred(name, args)
    return parse_eq()


def parse_eq():
    global line, cur
    e = parse_term()
    if line[cur] != '=':
        return None
    assert line[cur] == '='
    cur += 1
    return Eq(e, parse_term())



def parse_quan():
    global line, cur
    sym = line[cur]
    cur += 1
    var = ''
    while 'a' <= line[cur] <= 'z' or '0' <= line[cur] <= '9':
        var += line[cur]
        cur += 1
    tmp = parse_unar()
    if tmp is None:
        return None
    return Quan(sym, Var(var), tmp)


def parse_mul():
    global line, cur
    if line[cur] == '(':
        cur += 1
        e = parse_term()
        assert (line[cur] == ')')
        cur += 1
    else:  # 'a' <= line[cur] <= 'z' or '0':
        var = ''
        while cur < len(line) and ('a' <= line[cur] <= 'z' or '0' <= line[cur] <= '9'):
            var += line[cur]
            cur += 1
        if cur < len(line) and line[cur] == '(':
            cur += 1
            args = [parse_term()]
            while line[cur] == ',':
                cur += 1
                args.append(parse_term())
            assert (line[cur] == ')')
            cur += 1
            e = Fun(var, args)
        else:
            e = Var(var)
    while cur < len(line) and line[cur] == "'":
        cur += 1
        e = Plus_one(e)
    return e


def line_from_file(line1):
    global line, cur
    cur = 0
    line = line1


mod = 10 ** 9 + 7
cur = 0
# line = input()
# print(parse_exp())#.to_string())
