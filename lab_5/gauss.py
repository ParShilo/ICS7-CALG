import math

_cache = {}

def get_gauss_nodes_weights(degree):
    if degree in _cache:
        return _cache[degree]
    
    roots = []
    for i in range(1, degree + 1):
        x = math.cos((2*i - 1) / (2*degree) * math.pi)
        for _ in range(30):
            # P_n(x)
            p0, p1 = 1.0, x
            for k in range(2, degree + 1):
                p = ((2*k - 1)*x*p1 - (k - 1)*p0) / k
                p0, p1 = p1, p
            pn, pn1 = p1, p0
            
            # P'_n(x)
            if abs(x) >= 1.0: break
            dp = degree * (x*pn - pn1) / (x*x - 1)
            if abs(dp) < 1e-14: break
            x_new = x - pn / dp
            if abs(x_new - x) / max(1e-12, abs(x_new)) < 1e-12:
                x = max(-0.99999999, min(0.99999999, x_new))
                break
            x = x_new
        roots.append(x)
    roots.sort()
    
    weights = []
    for t in roots:
        p0, p1 = 1.0, t
        for k in range(2, degree + 1):
            p = ((2*k - 1)*t*p1 - (k - 1)*p0) / k
            p0, p1 = p1, p
        pn, pn1 = p1, p0
        dp = degree * (t*pn - pn1) / (t*t - 1)
        weights.append(2.0 / ((1 - t**2) * dp**2))
        
    _cache[degree] = (roots, weights)
    return roots, weights

def gauss_integral(f, a, b, degree, eps):
    t, w = get_gauss_nodes_weights(degree)
    def solve(N):
        h = (b - a) / N
        I = 0.0
        half = h / 2.0
        for i in range(N):
            mid = a + i*h + half
            for j in range(degree):
                I += w[j] * f(mid + half*t[j])
        return I * half

    N = 2
    I_N = solve(N)
    N = 4
    I_2N = solve(N)
    while abs(I_N - I_2N) > eps * max(1.0, abs(I_2N)) and N <= 128:
        I_N = I_2N
        N *= 2
        I_2N = solve(N)
    return I_2N

def gauss_integral_by_N(f, a, b, degree, N):
    t, w = get_gauss_nodes_weights(degree)
    h = (b - a) / N
    I = 0.0
    half = h / 2.0
    for i in range(N):
        mid = a + i*h + half
        for j in range(degree):
            I += w[j] * f(mid + half*t[j])
    return I * half