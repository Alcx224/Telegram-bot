from sympy import Symbol, Poly, solve

def solve_recurrence(g, f_coeffs, initial_conditions):
    k = len(initial_conditions)
    r = Symbol('r')
    eq = Poly(sum(f_coeffs[i] * r**(k-i) for i in range(k)), r)
    roots = solve(eq, r)

    constants = {}
    for i in range(k):
        constants['c{}'.format(i)] = initial_conditions[i]
        for j in range(i):
            constants['c{}'.format(i)] -= constants['c{}'.format(j)] * roots[i]**(j+1)

    solution = ''
    for i in range(k):
        term = '{} * {}^n'.format(constants['c{}'.format(i)], roots[i])
        solution += ' + ' + term if solution else term

    return 'f(n) = {}'.format(solution) + ' + {}'.format(g) if g else solution


def getvalues(to_g, to_f_coeffs, to_initial_conditions):
    g =str(to_g)
    f_coeffs=to_f_coeffs
    initial_conditions=to_initial_conditions
    return g, f_coeffs, initial_conditions



