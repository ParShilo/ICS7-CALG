import math

_cache = {}

def legendre_P(n, x):
    if n == 0: return 1.0
    if n == 1: return x
    p0, p1 = 1.0, x
    for k in range(2, n + 1):
        p = ((2*k - 1) * x * p1 - (k - 1) * p0) / k
        p0, p1 = p1, p
    return p

def legendre_P_prime(n, x):
    if abs(x) >= 1.0:
        return 0.0
    return n * (x * legendre_P(n, x) - legendre_P(n-1, x)) / (x*x - 1)

def get_gauss_nodes_weights(degree):
    if degree in _cache:
        return _cache[degree]
    
    roots = []
    for i in range(1, degree + 1):
        x = math.cos((2*i - 1) / (2*degree) * math.pi)
        for _ in range(50):
            p = legendre_P(degree, x)
            dp = legendre_P_prime(degree, x)
            if abs(dp) < 1e-14:
                break
            x_new = x - p / dp
            if abs(x_new - x) < 1e-12:
                x = max(-0.99999999, min(0.99999999, x_new))
                break
            x = x_new
        roots.append(x)
    roots.sort()
    
    T = [[r**k for r in roots] for k in range(degree)]
    F = [2.0 / (k + 1) if k % 2 == 0 else 0.0 for k in range(degree)]
    aug = [T[k][:] + [F[k]] for k in range(degree)]
    
    for col in range(degree):
        pivot = max(range(col, degree), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        piv = aug[col][col]
        for j in range(col, degree + 1):
            aug[col][j] /= piv
        for row in range(degree):
            if row != col:
                factor = aug[row][col]
                for j in range(col, degree + 1):
                    aug[row][j] -= factor * aug[col][j]
    
    weights = [aug[i][degree] for i in range(degree)]
    _cache[degree] = (roots, weights)
    return roots, weights


def gauss_integral(f, a, b, degree, eps):
    t, w = get_gauss_nodes_weights(degree)
    
    def solve(N):
        h = (b - a) / N
        I = 0.0
        for i in range(N):
            x0, x1 = a + i*h, a + (i+1)*h
            half = (x1 - x0) / 2.0
            mid = (x0 + x1) / 2.0
            for j in range(degree):
                x = mid + half * t[j]
                I += w[j] * f(x)
        return I * half
    
    N = 2
    I_N = solve(N)
    N *= 2
    I_2N = solve(N)
    
    while abs(I_N - I_2N) > eps * max(1.0, abs(I_2N)) and N <= 1024:
        I_N = I_2N
        N *= 2
        I_2N = solve(N)

    return I_2N


def gauss_integral_by_N(f, a, b, degree, N):
    t, w = get_gauss_nodes_weights(degree)
    h = (b - a) / N
    I = 0.0
    for i in range(N):
        x0, x1 = a + i*h, a + (i+1)*h
        half = (x1 - x0) / 2.0
        mid = (x0 + x1) / 2.0
        for j in range(degree):
            x = mid + half * t[j]
            I += w[j] * f(x)
    return I * half