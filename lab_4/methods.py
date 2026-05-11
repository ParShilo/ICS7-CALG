import math

def f1(x, y):
    return 20 * math.sin(0.7 * x + 0.7 * y) - 7 * x - 7 * y

def df1dx(x, y):
    return 14 * math.cos(0.7 * x + 0.7 * y) - 7

def df1dy(x, y):
    return 14 * math.cos(0.7 * x + 0.7 * y) - 7

def f2(x, y):
    return 20 * math.log(x) - 6 * y - x

def df2dx(x, y):
    return 20 / x - 1

def df2dy(x, y):
    return -6

def newton_method(x, y, eps, max_iter):
    delta = None

    for k in range(max_iter):
        try:
            F1 = f1(x, y)
            F2 = f2(x, y)

            j11, j12, j21, j22 = df1dx(x, y), df1dy(x, y), df2dx(x, y), df2dy(x, y)

            det_jacobian = j11 * j22 - j12 * j21
            if abs(det_jacobian) < 1e-12:
                raise ValueError("Определитель Якоби близок к нулю")

            dx = (-F1 * j22 + F2 * j12) / det_jacobian
            dy = (-j11 * F2 + j21 * F1) / det_jacobian

            x_new = x + dx
            y_new = y + dy

            if x_new <= 0:
                raise ValueError("В ходе итераций получено x ≤ 0")

            delta = math.sqrt(dx**2 + dy**2) / math.sqrt(x_new**2 + y_new**2)

            x, y = x_new, y_new

            if delta < eps:
                return x, y, k + 1, delta

        except:
            return None, None, None, None

    return x, y, max_iter, delta

# -------------------------------------------------------------------------

def f(t):
    return math.exp(-t*t/2)

def trapezoid(a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return h * s 

def integral(x, eps=1e-6, max_iter=50):
    if x == 0:
        return 0.0

    a = 0.0
    b = x

    n = 10

    I = trapezoid(a, b, n)

    for _ in range(max_iter):

        n *= 2
        I_new = trapezoid(a, b, n)

        delta = abs(I_new - I) / max(abs(I_new), 1e-12)

        if delta < eps:
            return I_new

        I = I_new

    return I_new 

def phi(x, eps=1e-6):
    return integral(x, eps) / math.sqrt(2 * math.pi)

def bisection_method(phi_value, eps, max_iter):

    if phi_value <= 0 or phi_value >= 0.5:
        return None, None, None

    a = 0.0
    b = 10.0

    def F(x):
        return phi(x) - phi_value

    if F(a) * F(b) > 0:
        return None, None, None

    for k in range(max_iter):
        c = (a + b) / 2
        Fc = F(c)

        if abs(b - a) / max(abs(c), 1e-12) < eps:
            return c, k + 1, abs(b - a)

        if F(a) * Fc < 0:
            b = c
        else:
            a = c

    return c, max_iter, abs(b - a)