import sys
from data import *
from data_for_not import *
sys.stdin = open('input.in', 'r')
sys.stdout = open('output.out', 'w')


def create_norm_proof(l, r):
    p = r - l
    l_formal = '0' + "'" * l
    r_formal = '0' + "'" * r
    p_formal = '0' + "'" * p

    rhs = '0'
    lhs = l_formal
    res = l_formal

    gip = '?p(' + l_formal + '+' + 'p' + '=' + r_formal + ')'
    print('|-' + gip)
    for i in swap_proof:
        print(i)
    for i in point_1_proof:
        print(i)
    for i in point_2_proof:
        print(i)
    for i in point_0_proof:
        print(i)

    print(point_0 + '->' + point_0_a.replace('a', lhs))

    for i in range(p):
        first = part_1.replace('a', lhs).replace('b', rhs).replace('c', res)
        print(first)
        print(point_1 + '->' + point_1_a.replace('a', lhs))
        print(point_1_a.replace('a', lhs))
        print(point_1_a.replace('a', lhs) + '->' + point_1_b.replace('a', lhs).replace('b', rhs))
        print(point_1_b.replace('a', lhs).replace('b', rhs))
        print(point_1_b.replace('a', lhs).replace('b', rhs) + '->' +
              point_1_c.replace('a', lhs).replace('b', rhs).replace('c', res))
        print(point_1_c.replace('a', lhs).replace('b', rhs).replace('c', res))

        print(part_2.replace('a', lhs).replace('b', rhs).replace('c', res))

        print(point_2 + '->' + point_2_a.replace('a', lhs))
        print(point_2_a.replace('a', lhs))
        print(point_2_a.replace('a', lhs) + '->' + point_2_b.replace('a', lhs).replace('b', rhs))
        print(point_2_b.replace('a', lhs).replace('b', rhs))
        print(point_2_b.replace('a', lhs).replace('b', rhs) + '->' +
              point_2_c.replace('a', lhs).replace('b', rhs).replace('c', res))
        print(point_2_c.replace('a', lhs).replace('b', rhs).replace('c', res))
        rhs += "'"
        res += "'"
    first = part_1.replace('a', lhs).replace('b', rhs).replace('c', res)
    print(first)
    print(first + '->' + gip)
    print(gip)


def create_proof_not(l, r):
    p = l - r
    l_formal = '0' + "'" * l
    r_formal = '0' + "'" * r
    p_formal = '0' + "'" * (p-1)

    rhs = p_formal
    res = '0'

    gip = '@p(!(' + 'p' + '+' + l_formal + '=' + r_formal + '))'
    print('|-' + gip)
    for i in swap_proof:
        print(i)
    for i in point_not_0_proof:
        print(i)
    for i in point_not_1_proof:
        print(i)
    for i in point_not_2_proof:
        print(i)
    for i in point_not_3_proof:
        print(i)

    print(point_not_0 + '->' + point_not_0_a.replace('a', 'p'+'+'+rhs))

    for i in range(p):
        #print('\nfirst')
        a = '(' + 'p' + '+' + rhs + ")'"
        b = 'p' + '+' + rhs + "'"
        first = part_not_1.replace('a', b[:-1]).replace('b', res)
        print(first)

        #print('\npoint 1')
        print(point_not_1 + '->' + point_not_1_a.replace('a', 'p'))
        print(point_not_1_a.replace('a', 'p'))
        print(point_not_1_a.replace('a', 'p') + '->' + point_not_1_b.replace('a', 'p').replace('b', rhs))
        print(point_not_1_b.replace('a', 'p').replace('b', rhs))

        #print('\npoint 2')
        print(point_not_2 + '->' + point_not_2_a.replace('a', a))
        print(point_not_2_a.replace('a', a))
        print(point_not_2_a.replace('a', a) + '->' + point_not_2_b.replace('a', a).replace('b', b))
        print(point_not_2_b.replace('a', a).replace('b', b))
        print(point_not_2_b.replace('a', a).replace('b', b) + '->' +
              point_not_2_c.replace('a', a).replace('b', b).replace('c', res))
        print(point_not_2_c.replace('a', a).replace('b', b).replace('c', res))

        #print('\nMP')
        print(part_not_2.replace('a', a).replace('b', b).replace('c', res))  # MP
        print(part_not_3.replace('b', b).replace('c', res))  # MP

        #print('\npoint 3')
        print(point_not_3 + '->' + point_not_3_a.replace('a', b))
        print(point_not_3_a.replace('a', b))
        print(point_not_3_a.replace('a', b) + '->' + point_not_3_b.replace('a', b).replace('b', res))
        print(point_not_3_b.replace('a', b).replace('b', res))

        rhs += "'"
        res += "'"

    #print('\nend')
    #print('\nfirst')
    a = '(' + 'p' + '+' + rhs + ")'"
    b = 'p' + '+' + rhs + "'"
    first = part_not_1.replace('a', b[:-1]).replace('b', res)
    print(first)

    #print('\npoint 1')
    print(point_not_1 + '->' + point_not_1_a.replace('a', 'p'))
    print(point_not_1_a.replace('a', 'p'))
    print(point_not_1_a.replace('a', 'p') + '->' + point_not_1_b.replace('a', 'p').replace('b', rhs))
    print(point_not_1_b.replace('a', 'p').replace('b', rhs))

    #print('\npoint 2')
    print(point_not_2 + '->' + point_not_2_a.replace('a', a))
    print(point_not_2_a.replace('a', a))
    print(point_not_2_a.replace('a', a) + '->' + point_not_2_b.replace('a', a).replace('b', b))
    print(point_not_2_b.replace('a', a).replace('b', b))
    print(point_not_2_b.replace('a', a).replace('b', b) + '->' +
          point_not_2_c.replace('a', a).replace('b', b).replace('c', res))
    print(point_not_2_c.replace('a', a).replace('b', b).replace('c', res))

    #print('\nMP')
    print(part_not_2.replace('a', a).replace('b', b).replace('c', res))  # MP
    print(part_not_3.replace('b', b).replace('c', res))  # MP
    print(gip[2:] + '->' + "(A->A->A)" + '->' + gip[2:])
    print("(A->A->A)" + '->' + gip[2:])
    print("(A->A->A)" + '->' + gip)
    print(gip)


def main():
    l, r = map(int, input().split())
    if l <= r:
        create_norm_proof(l, r)
    else:
        create_proof_not(l, r)

main()