def simpson_integral(f, a, b, eps):
    def solve(N):
        h = (b - a) / N
        I = 0.0
        for i in range(0, N, 2):
            I += f(a + i*h) + 4.0 * f(a + (i+1)*h) + f(a + (i+2)*h)
        return I * h / 3.0

    N = 2
    I_N = solve(N)
    N = 4
    I_2N = solve(N)
    while abs(I_N - I_2N) > eps * max(1.0, abs(I_2N)) and N <= 128:
        I_N = I_2N
        N *= 2
        I_2N = solve(N)

    return I_2N

def simpson_integral_by_N(f, a, b, N):
    if N % 2 != 0: N += 1
    h = (b - a) / N
    I = 0.0
    for i in range(0, N, 2):
        I += f(a + i*h) + 4.0 * f(a + (i+1)*h) + f(a + (i+2)*h)
    return I * h / 3.0