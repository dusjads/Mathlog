import time
from data import *
from my_parser import *

file_in = open('input.in', 'r', encoding='UTF-8')
file_out = open('output.out', 'w', encoding='UTF-8')


def create_proof(proof_type, line_check):
    global line_p, alpha, alpha_s
    if type(alpha) is Nothing:
        output.append(line_p.to_string())
        return
    if proof_type == 0:
        output.append(line_p.to_string())
        output.append(line_p.to_string() + '->' + alpha_s + '->' + line_p.to_string())
        output.append(alpha_s + '->' + line_p.to_string())
    elif proof_type == 1:
        dj = line_check.left.to_string()
        dji = line_check.to_string()
        di = line_p.to_string()
        output.append('(' + alpha_s + '->' + dj + ')' + '->' + '(' + '(' + alpha_s + '->' + dji +
                      ')' + '->' + alpha_s + '->' + di + ')')
        output.append('(' + '(' + alpha_s + '->' + dji +
                      ')' + '->' + alpha_s + '->' + di + ')')
        output.append(alpha_s + '->' + line_p.to_string())
    elif proof_type == 2:
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
    elif proof_type == 3:
        mapping = {"A": alpha, "B": line_check.left, "C": line_check.right,
                   "x": line_p.right.var}
        for i in range(len(any_proof)):
            output.append(proof_mapping(any_proof[i], mapping).to_string())
    elif proof_type == 4:
        mapping = {"A": alpha, "B": line_check.left, "C": line_check.right,
                   "x": line_p.left.var}
        for i in range(len(exists_proof)):
            output.append(proof_mapping(exists_proof[i], mapping).to_string())
    else:
        exit(1)


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
    return aks.hash == exp.hash


def check_mp():
    global lines, output, alpha_s, proof, line_p
    for i in range(len(lines) - 1, -1, -1):
        line_check = lines[i]
        if line_check.sym == '->' and line_check.right.is_equal(line_p) \
                and line_check.left.hash in proof.keys():
            create_proof(1, line_check)
            return True
    return False


def check_alpha():
    global lines, alpha_s, proof, line_p, alpha
    if line_p.is_equal(alpha):
        create_proof(2, '')
        return True
    return False


def check_gips():
    global gips, alpha_s, line_p
    for i in range(len(gips)):
        if line_p.is_equal(gips[i]):
            # print('(', count, ') ', line[:-1], ' (Предп. ', i + 1, ')', sep='', file=file_out)
            create_proof(0, '')

            return True
    return False


def check_axiom():
    global line_p, d, alpha_s
    for i in range(len(axioms)):
        axiom_check = axioms[i]
        d = dict()
        if ax_check(axiom_check, line_p):
            # print('(', count, ') ', line[:-1], ' (Сх. акс. ', i + 1, ')', sep='', file=file_out)
            create_proof(0, '')
            return True
    for i in range(len(formal_axioms)):
        formal_axiom_check = formal_axioms[i]
        d = dict()
        if check_formal(formal_axiom_check, line_p):
            # print('(', count, ') ', line[:-1], ' (Сх. акс. ', i + 1, ')', sep='', file=file_out)
            create_proof(0, '')
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
        if exp.name not in dictionary.keys():
            result.add(exp.name)
    elif type(exp) is Pred:
        for e in exp.args:
            get_free_variables(e, dictionary, result)
    elif type(exp) is Quan:
        if exp.var.name in dictionary.keys():
            dictionary[exp.var.name] += 1
        else:
            dictionary[exp.var.name] = 1
        get_free_variables(exp.args, dictionary, result)
        dictionary[exp.var.name] -= 1
        if dictionary[exp.var.name] == 0:
            dictionary.pop(exp.var.name)
    elif isinstance(exp, Unary):  # Plus_one or Negate
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
                locked[template.var.name] += 1
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
        elif isinstance(template, Unary):  # Plus_one or Negate
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
        create_proof(0, '')
        return True
    return False


def is_axiom_exists():
    global line_p, alpha_s
    if type(line_p) is not Exp or line_p.right.sym != '?':
        return False
    if free_subtract(line_p.right.args, line_p.left, line_p.right.var, dict(), dict()):
        create_proof(0, '')
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
        if var.name in get_free_variables(line_p.right, dict(), set()) \
                and free_subtract(tree_x1, tree_x_plus, var, dict(), dict()) \
                and free_subtract(tree_x1, tree_0, var, dict(), dict()) \
                and tree_x1.is_equal(tree_x2):
            create_proof(0, '')
            return True
    return False


def proof_mapping(expr, mapping):
    if type(expr) is Var:
        return mapping[expr.name]
    if type(expr) is Pred:
        return mapping[expr.name]

    if expr.sym == '->':
        return Exp(proof_mapping(expr.left, mapping), proof_mapping(expr.right, mapping))
    if expr.sym == '|':
        return Disj(proof_mapping(expr.left, mapping), proof_mapping(expr.right, mapping))
    if expr.sym == '&':
        return Conj(proof_mapping(expr.left, mapping), proof_mapping(expr.right, mapping))
    if expr.sym == '?' or expr.sym == '@':
        return Quan(expr.sym, proof_mapping(expr.var, mapping), proof_mapping(expr.args, mapping))


def check_quantifier():
    global line_p, lines, any_proof, exists_proof, alpha, error, alpha_s, free_from_alpha
    if line_p.sym != '->':
        return False
    for i in range(len(lines) - 2, -1, -1):
        line_check = lines[i]
        # Any
        if line_check.sym == '->' and line_p.right.sym == '@' and line_p.left.is_equal(line_check.left) \
                and line_check.right.is_equal(line_p.right.args):
            if line_p.right.var.name in free_from_alpha:
                error = 'невозможно преобразовать вывод, используется правило с квнтором по переменной ' + \
                        line_p.right.var.to_string() + \
                        ', входящей свободно в допущение ' + alpha_s
                return False
            if line_p.right.var.name in get_free_variables(line_p.left, dict(), set()):
                error = 'используется правило с квнтором по переменной ' + line_p.right.var.to_string() + \
                        ', входящей свободно в формулу ' + line_p.left.to_string()
                return False

            create_proof(3, line_check)
            return True
        # Exists
        if line_check.sym == '->' and line_p.left.sym == '?' and line_p.right.is_equal(line_check.right) \
                and line_check.left.is_equal(line_p.left.args):
            create_proof(4, line_check)
            return True
    return False


def main():
    global d, alpha_s, alpha, betta, line_p, lines, output, gips, any_proof, exists_proof, proof, free_from_alpha, error
    t1 = time.time()

    get_proofs()

    head_tmp = file_in.readline().replace(' ', '')
    head_tmp = head_tmp.replace(chr(13), '')
    head_tmp = head_tmp.replace('\n', '')
    output = []
    head = []
    balance = 0
    part = ''

    for i in range(len(head_tmp)):
        if head_tmp[i] == '(':
            balance += 1
            part += head_tmp[i]
        elif head_tmp[i] == ')':
            balance -= 1
            part += head_tmp[i]
        elif head_tmp[i] == ',' and balance == 0:
            head.append(part)
            part = ''
        else:
            part += head_tmp[i]
    head.append(part)
    gips = head[:-1] + head[-1].split('|-')
    betta = gips.pop()
    alpha = ''
    if len(gips) > 0 and gips[0] != '':
        alpha = gips.pop()
    s = ''
    for i in gips[:-1]:
        s += i + ','
    if alpha:
        s += (gips[-1] if len(gips) > 0 else '') + '|-' + '(' + alpha + ')' + '->' + '(' + betta + ')'
    else:
        s = '|-' + betta
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
    free_from_alpha = set()
    if type(alpha) is not Nothing:
        get_free_variables(alpha, dict(), free_from_alpha)

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
                        if not is_axiom_any():
                            if not is_axiom_exists():
                                if not check_induction():
                                    error = ''
                                    if not check_quantifier():
                                        if error:
                                            print('Вывод некорректен, начиная с формулы ', count, ': ', error, file=file_out)
                                            break
                                        print('Вывод некорректен, начиная с формулы ', count, ': ',
                                              'Недоказанное утверждение: ', line_p.to_string(), file=file_out, sep='')
                                        break

        proof[line_p.hash] = count
    else:
        print('Correct')
        for i in output:
            print(i, file=file_out)
    print(time.time() - t1)


main()
