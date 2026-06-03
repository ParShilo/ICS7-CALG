import numpy as np

def legendre_P(t, n):
    if n == 0: return 1.0
    if n == 1: return t
    p0, p1 = 1.0, t
    for k in range(2, n + 1):
        p = ((2*k - 1) * t * p1 - (k - 1) * p0) / k
        p0, p1 = p1, p
    return p

def get_intervals(degree):
    N = degree + 1
    if N % 2 != 0:
        N += 1

    h = 2 / (N - 1)
    x_values = [-1 + i * h for i in range(N)]

    changing_intervals = []
    while len(changing_intervals) != degree:
        changing_intervals.clear()
        for x1, x2 in zip(x_values[:-1], x_values[1:]):
            if legendre_P(x1, degree) * legendre_P(x2, degree) <= 0:
                changing_intervals.append((x1, x2))

        N *= 2
        h = 2 / (N - 1)
        x_values = [-1 + i * h for i in range(N)]

    return changing_intervals

def find_root(f, a, b, eps = 1e-10):
    c = (b + a) / 2
    fa, fc = f(a), f(c)

    while abs(b - a) > eps * max(1, abs(c)):
        if fa * fc < 0:
            b = c
        else:
            a, fa = c, fc
        c = (b + a) / 2
        fc = f(c)

    return c

def gauss_integral(f, a, b, degree, eps):
    root_intervals = get_intervals(degree)
    roots = [find_root(lambda t: legendre_P(t, degree), *interval) for interval in root_intervals]
    T = [[r ** k for r in roots] for k in range(degree)]
    F = [2 / (k + 1) if k % 2 == 0 else 0 for k in range(degree)]
    A = np.linalg.solve(T, F)

    def solve(N):
        h = (b - a) / N
        I = 0
        for i in range(N):
            x0, x1 = a + h * i, a + h * (i + 1)
            convert_to_x = lambda t: (x1 - x0) / 2 * t + (x1 + x0) / 2
            I += (x1 - x0) / 2 * sum([Ai * f(convert_to_x(t)) for t, Ai in zip(roots, A)])

        return I

    N = 2
    I_N = solve(N)
    N *= 2
    I_2N = solve(N)
    while abs(I_N - I_2N) > eps * abs(I_2N) and N <= 256:
        I_N = I_2N
        N *= 2
        I_2N = solve(N)

    return I_2N

def gauss_integral_by_N(f, a, b, degree, N):
    root_intervals = get_intervals(degree)
    roots = [find_root(lambda t: legendre_P(t, degree), *interval) for interval in root_intervals]

    T = [[r ** k for r in roots] for k in range(degree)]
    F = [2 / (k + 1) if k % 2 == 0 else 0 for k in range(degree)]
    A = np.linalg.solve(T, F)

    h = (b - a) / N
    I = 0
    for i in range(N):
        x0, x1 = a + h * i, a + h * (i + 1)
        convert_to_x = lambda t: (x1 - x0) / 2 * t + (x1 + x0) / 2
        I += (x1 - x0) / 2 * sum([Ai * f(convert_to_x(t)) for t, Ai in zip(roots, A)])

    return I
