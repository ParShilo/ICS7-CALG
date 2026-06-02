def simpson_integral(f, a, b, eps):
    def solve(N):
        h = (b - a) / N
        x_values = [a + i * h for i in range(N + 1)]
        I = 0.0
        for i in range(N // 2):
            I += f(x_values[2*i]) + 4.0 * f(x_values[2*i + 1]) + f(x_values[2*i + 2])
        return I * h / 3.0

    N = 2
    I_N = solve(N)
    N *= 2
    I_2N = solve(N)
    
    while abs(I_N - I_2N) > eps * max(1.0, abs(I_2N)) and N <= 1024:
        I_N = I_2N
        N *= 2
        I_2N = solve(N)

    return I_2N


def simpson_integral_by_N(f, a, b, N):
    if N % 2 != 0:
        N += 1
    h = (b - a) / N
    x_values = [a + i * h for i in range(N + 1)]
    I = 0.0
    for i in range(N // 2):
        I += f(x_values[2*i]) + 4.0 * f(x_values[2*i + 1]) + f(x_values[2*i + 2])
    return I * h / 3.0