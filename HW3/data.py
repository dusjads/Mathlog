swap = "@x@y(x=y->y=x)"
swap_x = "@y(x=y->y=x)"
swap_y = "(x=y->y=x)"

swap_proof = ["A->A->A",
              "a=b->a=c->b=c",
              "(a=b->a=c->b=c)->(A->A->A)->(a=b->a=c->b=c)",
              "(A->A->A)->(a=b->a=c->b=c)",
              "(A->A->A)->@c(a=b->a=c->b=c)",
              "(A->A->A)->@b@c(a=b->a=c->b=c)",
              "(A->A->A)->@a@b@c(a=b->a=c->b=c)",
              "@a@b@c(a=b->a=c->b=c)",
              "@a@b@c(a=b->a=c->b=c)->@b@c(x=b->x=c->b=c)",
              "@b@c(x=b->x=c->b=c)",
              "@b@c(x=b->x=c->b=c)->@c(x=y->x=c->y=c)",
              "@c(x=y->x=c->y=c)",
              "@c(x=y->x=c->y=c)->(x=y->x=z->y=z)",
              "x=y->x=z->y=z",
              "(x=y->x=z->y=z)->(A->A->A)->(x=y->x=z->y=z)",
              "(A->A->A)->(x=y->x=z->y=z)",
              "(A->A->A)->@z(x=y->x=z->y=z)",
              "(A->A->A)->@y@z(x=y->x=z->y=z)",
              "(A->A->A)->@x@y@z(x=y->x=z->y=z)",
              "@z(x=y->x=z->y=z)",
              "@z(x=y->x=z->y=z)->(x=y->x=x->y=x)",
              "x=y->x=x->y=x",
              "@x@y@z(x=y->x=z->y=z)",
              "@x@y@z(x=y->x=z->y=z)->@y@z(x+0=y->x+0=z->y=z)",
              "@y@z(x+0=y->x+0=z->y=z)",
              "@y@z(x+0=y->x+0=z->y=z)->@z(x+0=x->x+0=z->x=z)",
              "@z(x+0=x->x+0=z->x=z)",
              "@z(x+0=x->x+0=z->x=z)->(x+0=x->x+0=x->x=x)",
              "@a@b@c(a=b->a=c->b=c)->@b@c(x+0=b->x+0=c->b=c)",
              "@b@c(x+0=b->x+0=c->b=c)",
              "@b@c(x+0=b->x+0=c->b=c)->@c(x+0=x->x+0=c->x=c)",
              "@c(x+0=x->x+0=c->x=c)",
              "@c(x+0=x->x+0=c->x=c)->(x+0=x->x+0=x->x=x)",
              "x+0=x->x+0=x->x=x",
              "a+0=a",
              "(a+0=a)->(A->A->A)->(a+0=a)",
              "(A->A->A)->(a+0=a)",
              "(A->A->A)->@a(a+0=a)",
              "@a(a+0=a)",
              "@a(a+0=a)->(x+0=x)",
              "x+0=x",
              "x+0=x->x=x",
              "x=x",
              "x=x->x=y->x=x",
              "x=y->x=x",
              "(x=y->x=x)->(x=y->x=x->y=x)->(x=y->y=x)",
              "(x=y->x=x->y=x)->(x=y->y=x)",
              "x=y->y=x",
              "(x=y->y=x)->(A->A->A)->(x=y->y=x)",
              "(A->A->A)->(x=y->y=x)",
              "(A->A->A)->@y(x=y->y=x)",
              "(A->A->A)->@x@y(x=y->y=x)",
              "@x@y(x=y->y=x)"]

point_1 = "@a@b@c(a+b=c->(a+b)'=c')"  # A1
point_1_a = "@b@c(a+b=c->(a+b)'=c')"
point_1_b = "@c(a+b=c->(a+b)'=c')"
point_1_c = "(a+b=c->(a+b)'=c')"

point_1_proof = ["a=b->a'=b'",
                 "(a=b->a'=b')->(A->A->A)->(a=b->a'=b')",
                 "(A->A->A)->(a=b->a'=b')",
                 "(A->A->A)->@b(a=b->a'=b')",
                 "(A->A->A)->@a@b(a=b->a'=b')",
                 "@a@b(a=b->a'=b')",
                 "@a@b(a=b->a'=b')->@b(x=b->x'=b')",
                 "@b(x=b->x'=b')",
                 "@b(x=b->x'=b')->(x=y->x'=y')",
                 "(x=y->x'=y')",
                 "(x=y->x'=y')->(A->A->A)->(x=y->x'=y')",
                 "(A->A->A)->(x=y->x'=y')",
                 "(A->A->A)->@y(x=y->x'=y')",
                 "(A->A->A)->@x@y(x=y->x'=y')",
                 "@x@y(x=y->x'=y')",
                 "@x@y(x=y->x'=y')->@y(a+b=y->(a+b)'=y')",
                 "@y(a+b=y->(a+b)'=y')",
                 "@y(a+b=y->(a+b)'=y')->(a+b=c->(a+b)'=c')",
                 "(a+b=c->(a+b)'=c')",
                 "(a+b=c->(a+b)'=c')->(A->A->A)->(a+b=c->(a+b)'=c')",
                 "(A->A->A)->(a+b=c->(a+b)'=c')",
                 "(A->A->A)->@c(a+b=c->(a+b)'=c')",
                 "(A->A->A)->@b@c(a+b=c->(a+b)'=c')",
                 "(A->A->A)->@a@b@c(a+b=c->(a+b)'=c')",
                 "@a@b@c(a+b=c->(a+b)'=c')"
                 ]

point_2 = "@a@b@c((a+b)'=c'->a+b'=c')"
point_2_a = "@b@c((a+b)'=c'->a+b'=c')"
point_2_b = "@c((a+b)'=c'->a+b'=c')"
point_2_c = "((a+b)'=c'->a+b'=c')"

point_2_proof = ["a+b'=(a+b)'",
                 "@x@y(x=y->y=x)->@y(a+b'=y->y=a+b')",
                 "@y(a+b'=y->y=a+b')",
                 "@y(a+b'=y->y=a+b')->(a+b'=(a+b)'->(a+b)'=a+b')",
                 "a+b'=(a+b)'->(a+b)'=a+b'",
                 "a+b=c->(a+b)'=c'",
                 "@x@y@z(x=y->x=z->y=z)",
                 "@x@y@z(x=y->x=z->y=z)->@y@z((a+b)'=y->(a+b)'=z->y=z)",
                 "@y@z((a+b)'=y->(a+b)'=z->y=z)",
                 "@y@z((a+b)'=y->(a+b)'=z->y=z)->@z((a+b)'=a+b'->(a+b)'=z->a+b'=z)",
                 "@z((a+b)'=a+b'->(a+b)'=z->a+b'=z)",
                 "@z((a+b)'=a+b'->(a+b)'=z->a+b'=z)->((a+b)'=a+b'->(a+b)'=c'->a+b'=c')",
                 "(a+b)'=a+b'->(a+b)'=c'->a+b'=c'",
                 "(a+b)'=a+b'",
                 "(a+b)'=c'->a+b'=c'",
                 "((a+b)'=c'->a+b'=c')->(A->A->A)->((a+b)'=c'->a+b'=c')",
                 "(A->A->A)->((a+b)'=c'->a+b'=c')",
                 "(A->A->A)->@c((a+b)'=c'->a+b'=c')",
                 "(A->A->A)->@b@c((a+b)'=c'->a+b'=c')",
                 "(A->A->A)->@a@b@c((a+b)'=c'->a+b'=c')",
                 "@a@b@c((a+b)'=c'->a+b'=c')"]

point_0 = "@a(a+0=a)"
point_0_a = "(a+0=a)"

point_0_proof = ["a+0=a",
                 "(a+0=a)->(A->A->A)->(a+0=a)",
                 "(A->A->A)->(a+0=a)",
                 "(A->A->A)->@a(a+0=a)",
                 "@a(a+0=a)"]

part_1 = "a+b=c"
part_2 = "(a+b)'=c'"


