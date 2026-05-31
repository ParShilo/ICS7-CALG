def index_point(coords, target):
    idx = 0
    while idx + 1 < len(coords) and coords[idx] < target:
        idx += 1
    if idx > 0 and abs(coords[idx-1] - target) < abs(coords[idx] - target):
        idx -= 1
    return idx

def get_environment(coords, target, count):
    idx = index_point(coords, target)
    start = max(0, idx - count // 2)
    if start + count > len(coords):
        start = len(coords) - count
    return coords[start:start+count]

def newton_polynomial_1d(xs, ys, xq):
    n = len(xs)
    coef = list(ys)
    for j in range(1, n):
        for i in range(n - j):
            coef[i] = (coef[i+1] - coef[i]) / (xs[i+j] - xs[i])

    res = coef[0]
    term = 1.0
    for j in range(1, n):
        term *= (xq - xs[j-1])
        res += coef[j] * term
    return res

def newton_polynomial2D(Z, x_unique, y_unique, target_x, target_y, degree):
    x_nodes = get_environment(x_unique, target_x, degree + 1)
    z_at_x = []

    for x in x_nodes:
        y_nodes = get_environment(y_unique, target_y, degree + 1)
        z_vals = [Z[x][y] for y in y_nodes]
        z_at_x.append(newton_polynomial_1d(y_nodes, z_vals, target_y))

    return newton_polynomial_1d(x_nodes, z_at_x, target_x)