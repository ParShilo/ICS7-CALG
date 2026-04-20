def build_normal_system(x, y, rho, n):
    size = n + 1
    A = [[0.0 for _ in range(size)] for _ in range(size)]
    b = [0.0 for _ in range(size)]
    N = len(x)

    for m in range(size):
        for k in range(size):
            s = 0.0
            for i in range(N):
                s += rho[i] * (x[i] ** (m + k))
            A[m][k] = s

        s = 0.0
        for i in range(N):
            s += rho[i] * y[i] * (x[i] ** m)
        b[m] = s

    return A, b

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k

        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        for k in range(i + 1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    x_sol = [0.0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        s = b[i]
        for j in range(i + 1, n):
            s -= A[i][j] * x_sol[j]
        x_sol[i] = s / A[i][i]

    return x_sol

def least_squares(x, y, rho, n):
    A, b = build_normal_system(x, y, rho, n)
    coeffs = gaussian_elimination(A, b)
    return coeffs

def evaluate_polynomial(a, x_vals):
    y_vals = []
    for xi in x_vals:
        s = 0.0
        for k in range(len(a)):
            s += a[k] * (xi ** k)
        y_vals.append(s)
    return y_vals