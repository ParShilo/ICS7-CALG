import math

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

def gaussian_elimination(A, b, eps=1e-12):
    n = len(b)

    A = [row[:] for row in A]
    b = b[:]

    for i in range(n):
        max_row = i
        max_val = abs(A[i][i])

        for k in range(i + 1, n):
            if abs(A[k][i]) > max_val:
                max_val = abs(A[k][i])
                max_row = k

        if max_val < eps:
            raise ValueError("Матрица вырождена или плохо обусловлена.\n" "Возможно, степень полинома слишком велика (n >= N).")

        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]

        for k in range(i + 1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    x_sol = [0.0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        if abs(A[i][i]) < eps:
            raise ValueError("Деление на ноль при обратном ходе (матрица вырождена)")

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

#------------------------------------------

def get_basis_2d(degree):
    basis = []
    for i in range(degree + 1):
        for j in range(degree + 1 - i):
            basis.append(lambda xi, yi, _i=i, _j=j: (xi ** _i) * (yi ** _j))
    return basis

def least_squares_2d(x, y, z, rho, degree):
    basis = get_basis_2d(degree)
    m = len(basis)
    A = [[0.0] * m for _ in range(m)]
    b = [0.0] * m
    N = len(x)

    for j in range(m):
        for k in range(m):
            s = 0.0
            for i in range(N):
                s += rho[i] * basis[j](x[i], y[i]) * basis[k](x[i], y[i])
            A[j][k] = s
        s = 0.0
        for i in range(N):
            s += rho[i] * z[i] * basis[j](x[i], y[i])
        b[j] = s

    coeffs = gaussian_elimination(A, b)
    return coeffs, basis

def evaluate_polynomial_2d(coeffs, basis, xi, yi):
    return sum(c * func(xi, yi) for c, func in zip(coeffs, basis))

#------------------------------------------------

def fit_power(x, y):
# Степенная:  y = a * x^b 
    X = []
    Y = []
    rho = [1.0] * len(x)

    for i in range(len(x)):
        X.append(math.log(x[i]))
        Y.append(math.log(y[i]))

    coeffs = least_squares(X, Y, rho, 1)

    A = coeffs[0]
    b = coeffs[1]

    a = math.exp(A)

    return a, b

def fit_exponential(x, y):
# Экспонента: y = a * e^(bx)
    X = x[:]  
    Y = []
    rho = [1.0] * len(x)

    for i in range(len(x)):
        Y.append(math.log(y[i]))

    coeffs = least_squares(X, Y, rho, 1)

    A = coeffs[0]
    b = coeffs[1]

    a = math.exp(A)

    return a, b

def fit_fraction(x, y):
# Гипербола: y = a + b/x
    X = []
    Y = y[:]
    rho = [1.0] * len(x)

    for i in range(len(x)):
        X.append(1.0 / x[i])

    coeffs = least_squares(X, Y, rho, 1)

    a = coeffs[0]
    b = coeffs[1]

    return a, b

def fit_rational(x, y):
# Рациональная: y = a0 / (a1 + a2 * x)
    X = x[:]
    Y = []
    rho = [1.0] * len(x)

    for i in range(len(x)):
        Y.append(1.0 / y[i])

    coeffs = least_squares(X, Y, rho, 1)

    A = coeffs[0]
    B = coeffs[1]

    a0 = 1.0
    a1 = A
    a2 = B

    return a0, a1, a2

def compute_rms(y_true, y_pred):
    s = 0.0
    N = len(y_true)
    for i in range(N):
        s += (y_true[i] - y_pred[i]) ** 2
    return math.sqrt(s / N)

def eval_power(x, a, b):
    return [a * (xi ** b) for xi in x]

def eval_exponential(x, a, b):
    return [a * math.exp(b * xi) for xi in x]

def eval_fraction(x, a, b):
    return [a + b / xi for xi in x]

def eval_rational(x, a0, a1, a2):
    return [a0 / (a1 + a2 * xi) for xi in x]

#------------------------------------------------

def u0(x):
    return 1 - x

def du0(x):
    return -1.0

def d2u0(x):
    return 0.0

def uk(x, k):
    return x**k * (1 - x)

def duk(x, k):
    return k * x**(k - 1) - (k + 1) * x**k

def d2uk(x, k):
    if k == 1:
        return -2.0
    return k*(k-1)*x**(k-2) - k*(k+1)*x**(k-1)

# L[u] = u'' + x u' + u
def L_u0(x):
    return d2u0(x) + x * du0(x) + u0(x)

def L_uk(x, k):
    return d2uk(x, k) + x * duk(x, k) + uk(x, k)

def f_rhs(x):
    return 2 * x

def R0(x):
    return L_u0(x) - f_rhs(x)

def solve_bvp_least_squares(m, N_points=20):
    xs = [i / (N_points - 1) for i in range(N_points)]

    A = [[0.0 for _ in range(m)] for _ in range(m)]
    b = [0.0 for _ in range(m)]

    # alpha[i][k] = L[uk](x_i)
    alpha = []
    for xi in xs:
        row = []
        for k in range(1, m + 1):
            row.append(L_uk(xi, k))
        alpha.append(row)

    # R0 в точках
    R0_vals = [R0(xi) for xi in xs]

    for j in range(m):
        for k in range(m):
            s = 0.0
            for i in range(N_points):
                s += alpha[i][k] * alpha[i][j]
            A[j][k] = s

    for j in range(m):
        s = 0.0
        for i in range(N_points):
            s += R0_vals[i] * alpha[i][j]
        b[j] = -s

    C = gaussian_elimination(A, b)

    return C

def evaluate_bvp_solution(x_vals, C):
    y_vals = []

    for x in x_vals:
        s = u0(x)
        for k, c in enumerate(C, start=1):
            s += c * uk(x, k)
        y_vals.append(s)

    return y_vals