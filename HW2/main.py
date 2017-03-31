import time
from data import *
from my_parser import *

file_in = open('input.in', 'r', encoding='UTF-8')
file_out = open('output.out', 'w', encoding='UTF-8')


def ax_check(aks, exp):
    global d
    if not aks.sym:
        if aks.hash in d.keys():
            return d[aks.hash].is_equal(exp)
        d[aks.hash] = exp
        return True
    if aks.sym == '!':
        if '!' == exp.sym:
            return ax_check(aks.args, exp.args)
        return False
    if aks.sym == exp.sym:
        return ax_check(aks.left, exp.left) and ax_check(aks.right, exp.right)
    return False


def check_formal(aks, exp):
    global d
    if not aks.sym:
        if aks.hash in d.keys():
            return d[aks.hash].is_equal(exp)
        d[aks.hash] = exp
        return True
    if isinstance(aks, Unary):
        if type(aks) is type(exp):
            return check_formal(aks.args, exp.args)
        return False
    if aks.sym == exp.sym:
        return check_formal(aks.left, exp.left) and check_formal(aks.right, exp.right)
    return False


def check_mp():
    global lines, output, alpha_s, proof, line_p
    for i in range(len(lines) - 1, -1, -1):
        line_check = lines[i]
        if line_check.sym == '->' and line_check.right.is_equal(line_p) \
                and line_check.left.hash in proof.keys():
            dj = line_check.left.to_string()
            dji = line_check.to_string()
            di = line_p.to_string()
            output.append('(' + alpha_s + '->' + dj + ')' + '->' + '(' + '(' + alpha_s + '->' + dji +
                          ')' + '->' + alpha_s + '->' + di + ')')
            output.append('(' + '(' + alpha_s + '->' + dji +
                          ')' + '->' + alpha_s + '->' + di + ')')
            output.append(alpha_s + '->' + line_p.to_string())
            return True
    return False


def create_proof(expr, mapping):
    if type(expr) is Var:
        return mapping[expr.name]
    if type(expr) is Pred:
        return mapping[expr.name]

    if expr.sym == '->':
        return Exp(create_proof(expr.left, mapping), create_proof(expr.right, mapping))
    if expr.sym == '|':
        return Disj(create_proof(expr.left, mapping), create_proof(expr.right, mapping))
    if expr.sym == '&':
        return Conj(create_proof(expr.left, mapping), create_proof(expr.right, mapping))
    if expr.sym == '?' or expr.sym == '@':
        return Quan(expr.sym, create_proof(expr.var, mapping), create_proof(expr.args, mapping))


def check_quantifier():
    global line_p, lines, any_proof, exists_proof, alpha, output
    if line_p.sym != '->':
        return False
    for i in range(len(lines) - 1, -1, -1):
        line_check = lines[i]
        # Any
        if line_check.sym == '->' and line_p.right.sym == '@' and line_p.left.is_equal(line_check.left) \
                and line_check.right.is_equal(line_p.right.args):
            mapping = {"A": alpha, "B": line_check.left, "C": line_check.right,
                       "x": line_p.right.var}
            for i in range(len(any_proof)):
                output.append(create_proof(any_proof[i], mapping).to_string())
            return True
        # Exists
        if line_check.sym == '->' and line_p.left.sym == '?' and line_p.right.is_equal(line_check.right) \
                and line_check.left.is_equal(line_p.left.args):
            mapping = {"A": alpha, "B": line_check.left, "C": line_check.right,
                       "x": line_p.left.var}
            for i in range(len(exists_proof)):
                output.append(create_proof(exists_proof[i], mapping).to_string())
            return True
    return False


def check_alpha():
    global lines, output, alpha_s, proof, line_p, alpha
    if line_p.is_equal(alpha):
        output.append(alpha_s + '->' + alpha_s + '->' + alpha_s)
        output.append('(' + alpha_s + '->' + alpha_s + '->' + alpha_s + ')' + '->' + '(' + alpha_s + '->' +
                      '(' + '(' + alpha_s + '->' + alpha_s + ')' + '->' + alpha_s + ')' + ')' + '->' +
                      '(' + alpha_s + '->' + alpha_s + ')')
        output.append('(' + alpha_s + '->' +
                      '(' + '(' + alpha_s + '->' + alpha_s + ')' + '->' + alpha_s + ')' + ')' + '->' +
                      '(' + alpha_s + '->' + alpha_s + ')')
        output.append('(' + alpha_s + '->' +
                      '(' + '(' + alpha_s + '->' + alpha_s + ')' + '->' + alpha_s + ')' + ')')
        output.append(alpha_s + '->' + alpha_s)
        return True
    return False


def check_gips():
    global gips, alpha_s, line_p
    for i in range(len(gips)):
        if line_p.is_equal(gips[i]):
            # print('(', count, ') ', line[:-1], ' (Предп. ', i + 1, ')', sep='', file=file_out)
            output.append(line_p.to_string())
            output.append(line_p.to_string() + '->' + alpha_s + '->' + line_p.to_string())
            output.append(alpha_s + '->' + line_p.to_string())
            return True
    return False


def check_axiom():
    global line_p, d, alpha_s
    for i in range(len(axioms)):
        axiom_check = axioms[i]
        d = dict()
        if ax_check(axiom_check, line_p):
            # print('(', count, ') ', line[:-1], ' (Сх. акс. ', i + 1, ')', sep='', file=file_out)
            output.append(line_p.to_string())
            output.append(line_p.to_string() + '->' + alpha_s + '->' + line_p.to_string())
            output.append(alpha_s + '->' + line_p.to_string())
            return True
    for i in range(len(formal_axioms)):
        formal_axiom_check = formal_axioms[i]
        d = dict()
        if check_formal(formal_axiom_check, line_p):
            # print('(', count, ') ', line[:-1], ' (Сх. акс. ', i + 1, ')', sep='', file=file_out)
            output.append(line_p.to_string())
            output.append(line_p.to_string() + '->' + alpha_s + '->' + line_p.to_string())
            output.append(alpha_s + '->' + line_p.to_string())
            return True
    return False


def get_proofs():
    global any_proof, exists_proof
    fany = open("any_rule.proof", "r")
    any_proof = fany.readlines()
    fany.close()
    for i in range(len(any_proof)):
        line_from_file(any_proof[i])
        any_proof[i] = parse_exp()
    fexists = open("exists_rule.proof", "r")
    exists_proof = fexists.readlines()
    fexists.close()
    for i in range(len(exists_proof)):
        line_from_file(exists_proof[i])
        exists_proof[i] = parse_exp()


def get_free_variables(exp, dictionary: dict, result: set):
    if type(exp) is Var:
        if exp not in dictionary.keys():
            result.add(exp.name)
    elif type(exp) is Pred:
        for e in exp.args:
            get_free_variables(e, dictionary, result)
    elif type(exp) is Quan:
        if exp.var in dictionary.keys():
            dictionary[exp.var] += 1
        else:
            dictionary[exp.var] = 1
        get_free_variables(exp.args, dictionary, result)
        dictionary[exp.var] -= 1
        if dictionary[exp.var] == 0:
            dictionary.pop(exp.var)
    elif isinstance(exp, Unary):
        get_free_variables(exp.args, dictionary, result)
    else:
        get_free_variables(exp.left, dictionary, result)
        get_free_variables(exp.right, dictionary, result)
    return result


def free_subtract(template, exp, var, locked: dict, dictionary):
    if type(template) is Var:
        if not template.is_equal(var):
            return template.is_equal(exp)
        if template.name in locked:
            return template.is_equal(exp)
        else:
            if template in dictionary:
                return dictionary[template].is_equal(exp)
            else:
                tmp = set()
                get_free_variables(exp, dict(), tmp)
                if len(tmp.intersection(locked)) != 0:
                    return False
                dictionary[template] = exp
                return True
    elif type(template) is type(exp):
        if type(template) is Quan:
            if template.var.name not in locked:
                locked[template.var.name] = 1
            else:
                locked[template.var.args] += 1
            result = free_subtract(template.args, exp.args, var, locked, dictionary)
            locked[template.var.name] -= 1
            if locked[template.var.name] == 0:
                locked.pop(template.var.name, None)
            return result
        elif type(template) is Pred:
            if len(template.args) != len(exp.args):
                return False
            for i in range(len(template.args)):
                if not free_subtract(template.args[i], exp.args[i], var, locked, dictionary):
                    return False
            return True
        elif isinstance(template, Unary):
            return free_subtract(template.args, exp.args, var, locked, dictionary)

        else:
            if not free_subtract(template.left, exp.left, var, locked, dictionary):
                return False
            return free_subtract(template.right, exp.right, var, locked, dictionary)
    else:
        return False


def is_axiom_any():
    global line_p, alpha_s
    if type(line_p) is not Exp or line_p.left.sym != '@':
        return False
    if free_subtract(line_p.left.args, line_p.right, line_p.left.var, dict(), dict()):
        output.append(line_p.to_string())
        output.append(line_p.to_string() + '->' + alpha_s + '->' + line_p.to_string())
        output.append(alpha_s + '->' + line_p.to_string())
        return True
    return False


def is_axiom_exists():
    global line_p, alpha_s
    if type(line_p) is not Exp or line_p.right.sym != '?':
        return False
    if free_subtract(line_p.right.args, line_p.left, line_p.right.var, dict(), dict()):
        output.append(line_p.to_string())
        output.append(line_p.to_string() + '->' + alpha_s + '->' + line_p.to_string())
        output.append(alpha_s + '->' + line_p.to_string())
        return True
    return False

def check_induction():
    global line_p
    if type(line_p) is Exp \
            and type(line_p.left) is Conj \
            and line_p.left.right.sym == '@' \
            and type(line_p.left.right.args) is Exp:
        var = line_p.left.right.var
        tree_0 = line_p.left.left
        tree_x1 = line_p.right
        tree_x2 = line_p.left.right.args.left
        tree_x_plus = line_p.left.right.args.right
        print('So', line_p.to_string())
        if var.name in get_free_variables(line_p.right, dict(), set()) \
            and free_subtract(tree_x1, tree_x_plus, Var(var), dict(), dict()) \
            and free_subtract(tree_x1, tree_0, Var(var), dict(), dict()) \
            and tree_x1.is_eqal(tree_x2):
            print('Yes')
            return True
    return False




def main():
    global d, alpha_s, alpha, betta, line_p, lines, output, gips, any_proof, exists_proof, proof
    t1 = time.time()

    get_proofs()

    head = file_in.readline().replace(' ', '')
    head = head.replace(chr(13), '')
    head = head.replace('\n', '')
    output = []
    head = list(head.split(','))
    gips = head[:-1] + head[-1].split('|-')
    betta = gips.pop()
    alpha = ''
    print(gips)
    if len(gips) > 0 and gips[0] != '':
        alpha = gips.pop()
    s = ''
    for i in gips[:-1]:
        s += i + ','
    if alpha:
        s += (gips[-1] if len(gips) > 0 else '') + '|-' + '(' + alpha + ')' + '->' + '(' + betta + ')'
    else:
        s = '|-' + betta
    print(s)
    output.append(s)

    if len(gips) == 0 or not gips[0]:
        gips = []
    for i in range(len(gips)):
        line_from_file(gips[i])
        gips[i] = parse_exp()
    if alpha:
        line_from_file(alpha)
        alpha = parse_exp()
        alpha_s = alpha.to_string()
    else:
        alpha = Nothing()
    line_from_file(betta)
    betta = parse_exp()
    count = 0
    lines = []
    proof = dict()
    for line in file_in:
        if line[-1] != "\n":
            line += "\n"
        count += 1
        line = line.replace(' ', '')
        line = line.replace(chr(13), '')
        line_from_file(line)
        line_p = parse_exp()
        lines.append(line_p)
        if not check_gips():
            if not check_axiom():
                if not check_alpha():
                    if not check_mp():
                        if not check_quantifier():
                            if not is_axiom_any():
                                if not is_axiom_exists():
                                    if not check_induction():
                                        print('(', count, ') ', line[:-1], ' (Не доказано)', sep='')
                                        print(line_p.to_string())

        proof[line_p.hash] = count
    print(time.time() - t1)
    for i in output:
        print(i, file=file_out)


main()
