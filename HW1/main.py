import time

from my_parser import *

file_in = open('input.in', 'r', encoding='UTF-8')
file_out = open('output.out', 'w', encoding='UTF-8')


def check(aks, exp):
    global d
    if not aks.sym:
        if aks.hash in d.keys():
            return d[aks.hash].is_equal(exp)
        d[aks.hash] = exp
        return True
    if aks.sym == '!':
        if '!' == exp.sym:
            return check(aks.var, exp.var)
        return False
    if aks.sym == exp.sym:
        return check(aks.left, exp.left) and check(aks.right, exp.right)
    return False


def main():
    global d
    t1 = time.time()

    aksioms = ['A->B->A', '(A->B)->(A->B->C)->(A->C)', 'A->B->A&B', 'A&B->A', 'A&B->B',
               'A->A|B', 'B->A|B', '(A->C)->(B->C)->(A|B->C)', '(A->B)->(A->!B)->!A', '!!A->A']

    for i in range(len(aksioms)):
        line_from_file(aksioms[i])
        aksioms[i] = parse_exp()

    head = file_in.readline().replace(' ', '')
    head = head.replace(chr(13), '')
    print(head, file=file_out, end='')
    head = list(head.split(','))
    gips = head[:-1] + head[-1].split('|-')
    res = gips.pop()

    if not gips[0]:
        gips = []
    for i in range(len(gips)):
        line_from_file(gips[i])
        gips[i] = parse_exp()

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
        for i in range(len(gips)):
            if line_p.is_equal(gips[i]):
                print('(', count, ') ', line[:-1], ' (Предп. ', i + 1, ')', sep='', file=file_out)
                break
        else:
            for i in range(len(lines)):
                line_check = lines[i]
                if line_check.sym == '->' and line_check.right.is_equal(
                        line_p) and line_check.left.hash in proof.keys():
                    print('(', count, ') ', line[:-1], ' (M.P. ', proof[line_check.left.hash], ', ', i + 1, ')', sep='',
                          file=file_out)
                    break
            else:
                for i in range(len(aksioms)):
                    aksiom_check = aksioms[i]
                    d = dict()
                    if check(aksiom_check, line_p):
                        print('(', count, ') ', line[:-1], ' (Сх. акс. ', i + 1, ')', sep='', file=file_out)
                        break
                else:
                    print('(', count, ') ', line[:-1], ' (Не доказано)', sep='', file=file_out)

        proof[line_p.hash] = count
    print(time.time() - t1)


main()
