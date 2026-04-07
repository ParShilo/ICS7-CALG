def cubic_spline_1d(table, target_x):
    n = len(table) - 1
    if n < 1:
        return table[0][1]

    x = [p[0] for p in table]
    y = [p[1] for p in table]

    h = [x[i + 1] - x[i] for i in range(n)]

    c = [0.0] * (n + 1)
    c[0] = 0
    c[n] = 0

    if n >= 2:
        size = n - 1

        lower = [0.0] * size
        diag = [0.0] * size
        upper = [0.0] * size
        rhs = [0.0] * size

        for i in range(size):
            idx = i + 1
            diag[i] = 2.0 * (h[idx - 1] + h[idx])
            rhs[i] = 3.0 * ((y[idx + 1] - y[idx]) / h[idx] - (y[idx] - y[idx - 1]) / h[idx - 1])
            if i > 0:
                lower[i] = h[idx - 1]
            if i < size - 1:
                upper[i] = h[idx]

        rhs[0] -= h[0] * c[0]
        rhs[size - 1] -= h[n - 1] * c[n]

        xi = [0.0] * size
        eta = [0.0] * size

        xi[0] = -upper[0] / diag[0]
        eta[0] = rhs[0] / diag[0]

        for i in range(1, size):
            denom = diag[i] + lower[i] * xi[i - 1]
            xi[i] = -upper[i] / denom if i < size - 1 else 0.0
            eta[i] = (rhs[i] - lower[i] * eta[i - 1]) / denom

        c_inner = [0.0] * size
        c_inner[-1] = eta[-1]
        for i in range(size - 2, -1, -1):
            c_inner[i] = xi[i] * c_inner[i + 1] + eta[i]

        for i in range(size):
            c[i + 1] = c_inner[i]

    a = [y[i] for i in range(n)]
    b = [0.0] * n
    d = [0.0] * n

    for i in range(n):
        d[i] = (c[i + 1] - c[i]) / (3.0 * h[i])
        b[i] = (y[i + 1] - y[i]) / h[i] - h[i] * (2.0 * c[i] + c[i + 1]) / 3.0

    k = n - 1
    for i in range(n):
        if target_x <= x[i + 1]:
            k = i
            break

    if target_x < x[0]:
        k = 0
    if target_x > x[-1]:
        k = n - 1

    dx = target_x - x[k]
    result = a[k] + b[k] * dx + c[k] * dx ** 2 + d[k] * dx ** 3

    return result
