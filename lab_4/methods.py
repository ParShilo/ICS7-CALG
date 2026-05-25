import math

def f1(x, y):
    return 20 * math.log(x - y) - x - y - 6

def df1dx(x, y):
    return 20 / (x - y) - 1

def df1dy(x, y):
    return -20 / (x - y) - 1

def f2(x, y):
    return 20 * math.sin(0.7 * x - 0.7 * y) + 7 * x + 7 * y

def df2dx(x, y):
    return 14 * math.cos(0.7 * x - 0.7 * y) + 7

def df2dy(x, y):
    return -14 * math.cos(0.7 * x - 0.7 * y) + 7

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

            if x_new - y_new <= 0:
                raise ValueError("Нарушена область определения: x - y должно быть > 0")
            
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

def integral(x, eps=1e-8, max_iter=100):
    if x == 0:
        return 0.0

    a = 0.0
    b = x

    n = 20

    I = trapezoid(a, b, n)

    for _ in range(max_iter):

        n *= 2
        I_new = trapezoid(a, b, n)

        delta = abs(I_new - I) / abs(I_new)

        if delta < eps:
            return I_new

        I = I_new

    return I_new 

def phi(x):
    return 2 * integral(x) / math.sqrt(2 * math.pi)

def bisection_method(phi_value, eps, max_iter):

    if phi_value <= 0 or phi_value >= 1:
        return None, None, None

    a = 0.0
    b = 10

    def F(x):
        return phi(x) - phi_value

    if F(a) * F(b) > 0:
        return None, None, None

    for k in range(max_iter):
        c = (a + b) / 2
        Fc = F(c)

        if abs(b - a) / max(1e-12, abs(c)) < eps:
            return c, k + 1, abs(b - a)

        if Fc > 0:
            b = c
        else:
            a = c

        #print(f"{a}, {b}")
        #print(f"{F(a)}, {F(b)}")

    return c, max_iter, abs(b - a)

# ------------------------------------------------------------------

def solve_task3_newton_progonka(N=20, eps_newton=1e-8, max_newton_iter=50):
    h = 1.0 / N
    x_nodes = [i * h for i in range(N + 1)]
    
    y = [1.0 + 2.0 * xi for xi in x_nodes]
    
    M = N - 1
    
    for it in range(max_newton_iter):
        A = [1.0] * M
        B = [0.0] * M
        D = [1.0] * M
        F = [0.0] * M
        
        for i in range(M):
            n = i + 1
            yn = y[n]
            
            B[i] = -2.0 - 3.0 * h**2 * yn**2
            
            G_n = y[n-1] - 2.0*yn + y[n+1] - h**2 * yn**3 - h**2 * x_nodes[n]**2
            F[i] = -G_n 
            
        xi = [0.0] * (M + 2)
        eta = [0.0] * (M + 2)
        
        xi[1] = 0.0
        eta[1] = 0.0
        
        for i in range(1, M + 1):
            idx = i - 1
            denom = A[idx] * xi[i] + B[idx]
            
            if abs(denom) < 1e-15:
                raise ValueError("Деление на ноль в прямом ходе прогонки")
                
            xi[i+1] = -D[idx] / denom
            eta[i+1] = (F[idx] - A[idx] * eta[i]) / denom
            
        delta_y = [0.0] * (M + 2)
        delta_y[M+1] = 0.0
        
        for i in range(M, 0, -1):
            delta_y[i] = xi[i+1] * delta_y[i+1] + eta[i+1]
            
        max_delta = 0.0
        for i in range(M):
            y[i+1] += delta_y[i+1]
            max_delta = max(max_delta, abs(delta_y[i+1]))
            
        if max_delta < eps_newton:
            break
            
    return x_nodes, y