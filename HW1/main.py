import sys
import time

from my_parser import *

sys.stdin = open('input.in', 'r')
sys.stdout = open('output.out', 'w', encoding='UTF-8')


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

    head = list(input().split(','))
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
    for line in sys.stdin:
        if line[-1] != "\n":
            line += "\n"
        count += 1
        line_from_file(line)
        line_p = parse_exp()
        lines.append(line_p)
        for i in range(len(gips)):
            if line_p.is_equal(gips[i]):
                print('(', count, ') ', line[:-1], ' (Предп. ', i + 1, ')', sep='')
                break
        else:
            for i in range(len(lines)):
                line_check = lines[i]
                if line_check.sym == '->' and line_check.right.is_equal(
                        line_p) and line_check.left.hash in proof.keys():
                    print('(', count, ') ', line[:-1], ' (M.P. ', proof[line_check.left.hash], ', ', i + 1, ')', sep='')
                    break
            else:
                for i in range(len(aksioms)):
                    aksiom_check = aksioms[i]
                    d = dict()
                    if check(aksiom_check, line_p):
                        print('(', count, ') ', line[:-1], ' (Сх. акс. ', i + 1, ')', sep='')
                        break
                else:
                    print('(', count, ') ', line[:-1], ' Не доказано', sep='')

        proof[line_p.hash] = count
    print(time.time() - t1)


main()
