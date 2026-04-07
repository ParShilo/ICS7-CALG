import math

EPS = 1e-5

def get_index(table, target_x):
    ind = 0
    while ind + 1 < len(table) and table[ind][0] < target_x:
        ind += 1

    if ind > 0:
        cur_diff = abs(table[ind][0] - target_x)
        prev_diff = abs(table[ind - 1][0] - target_x)
        if prev_diff < cur_diff:
            ind -= 1

    return ind

def get_points(table, target_x, count):
    center = get_index(table, target_x)

    start = center - count // 2
    end = center + math.ceil(count / 2)

    if start < 0:
        end += -start
        start = 0

    if end > len(table):
        start -= end - len(table)
        end = len(table)

    start = max(start, 0)
    return table[start:end]

def divided_difference(x1, x2, y1, y2):
    return (y1 - y2) / (x1 - x2)

def newton_interpolation(table, target_x, n):
    # Определение конфигурации
    n = min(n, len(table) - 1)
    points = get_points(table, target_x, n + 1)
    coefs = [points[0][1]]

    # Расчёт коэффициентов полинома Ньютона
    values = [y for _, y in points]
    for i in range(n, 0, -1):
        ind = n + 1 - i
        for j in range(i):
            x1 = points[j][0]
            x2 = points[j + ind][0]
            y1 = values[j]
            y2 = values[j + 1]
            values[j] = divided_difference(x1, x2, y1, y2)
        coefs.append(values[0])

    # Вычисление значения самого полинома
    x = 1.0
    y = 0.0
    for i in range(len(points)):
        y += coefs[i] * x
        x *= target_x - points[i][0]

    return y

def newton_interpolation_2d(table, target_x, target_y, n):
    x_values = []
    for x, _, _ in table:
        if x not in x_values:
            x_values.append(x)

    xz = []
    for current_x in x_values:
        yz = []
        for x, y, z in table:
            if (x == current_x):
                yz.append((y, z))
        y_degree = min(n, len(yz) - 1)
        xz.append((current_x, newton_interpolation(yz, target_y, y_degree)))

    x_degree = min(n, len(xz) - 1)
    return newton_interpolation(xz, target_x, x_degree)

def calculate_p(T, K, Nh_table, degree):
    a, b = 0.3, 2.5
    fa = newton_interpolation_2d(Nh_table, T, a, degree) - K
    fb = newton_interpolation_2d(Nh_table, T, b, degree) - K
    if abs(fa) < EPS:
        return a
    if abs(fb) < EPS:
        return b
    while b - a > EPS:
        c = (a + b) / 2
        fc = newton_interpolation_2d(Nh_table, T, c, degree) - K
        if abs(fc) < EPS:
            return c
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    return (a + b) / 2

def calculate_phi(t, T, p, I_table, sigma_table, q_table, c_table, degree, R):
    I = newton_interpolation(I_table, t, degree)
    j = I / (math.pi * R**2)
    sigma = newton_interpolation_2d(sigma_table, T, p, degree)
    q = newton_interpolation_2d(q_table, T, p, degree)
    c = newton_interpolation_2d(c_table, T, p, degree)
    return (j**2 / sigma - q) / c

def rk2_step(t, T, dt, K_const, I_table, Nh_table, sigma_table, q_table, c_table, degree, R):
    p_n = calculate_p(T, K_const, Nh_table, degree)
    T_half = T + dt * calculate_phi(t, T, p_n, I_table, sigma_table, q_table, c_table, degree, R)
    p_half = calculate_p(T_half, K_const, Nh_table, degree)
    T_new = T + dt * calculate_phi(t + dt/2, T_half, p_half, I_table, sigma_table, q_table, c_table, degree, R)
    return T_new