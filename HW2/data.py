from my_parser import *

axioms = [
    'A->B->A',
    '(A->B)->(A->B->C)->(A->C)',
    'A->B->A&B',
    'A&B->A',
    'A&B->B',
    'A->A|B',
    'B->A|B',
    '(A->C)->(B->C)->(A|B->C)',
    '(A->B)->(A->!B)->!A',
    '!!A->A']

formal_axioms = [
    "a=b->a'=b'",
    "a=b->a=c->b=c",
    "a'=b'->a=b",
    "!(a'=0)",
    "a+b'=(a+b)'",
    "a+0=a",
    "a*0=0",
    "a*b'=a*b+a"
]


for i in range(len(axioms)):
    line_from_file(axioms[i])
    axioms[i] = parse_exp()

for i in range(len(formal_axioms)):
    line_from_file(formal_axioms[i])
    formal_axioms[i] = parse_exp()

