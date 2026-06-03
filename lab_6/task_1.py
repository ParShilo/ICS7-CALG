
def left_diff(y_p, y_c, h):
    return (y_c - y_p) / h

def right_diff(y_c, y_n, h):
    return (y_n - y_c) / h

def central_diff(y_p, y_n, h):
    return (y_n - y_p) / h

def second_diff(y_p, y_c, y_n, h):
    return (y_p - 2 * y_c + y_n) / (h ** 2)

def runge_left_diff(y_pp, y_p, y_c, h):
    """ 2 * f'(h) - f'(2h) """
    d = left_diff(y_p, y_c, h)
    d2 = left_diff(y_pp, y_c, 2 * h)
    return 2 * d - d2

def runge_right_diff(y_c, y_n, y_nn, h):
    """ 2 * f'(h) - f'(2h) """
    d = right_diff(y_c, y_n, h)
    d2 = right_diff(y_c, y_nn, 2 * h)
    return 2 * d - d2

def aligned_diff(x_vals, y_vals):
    xi = [1.0 / x for x in x_vals]
    eta = [1.0 / y for y in y_vals]
    
    d_new = [0.0] * len(x_vals)
    for i in range(len(x_vals) - 1):
        d_new[i] = (eta[i + 1] - eta[i]) / (xi[i + 1] - xi[i])
    d_new[-1] = (eta[-1] - eta[-2]) / (xi[-1] - xi[-2])
    
    res = []
    for i in range(len(x_vals)):
        res.append(d_new[i] * (y_vals[i] ** 2) / (x_vals[i] ** 2))
    return res

def printf(val):
    if val is None:
        return "           "
    return f"{val:^11.6f}"

def run_task_1():    
    x = [1, 2, 3, 4, 5, 6]
    y = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]
    n = len(x)
    h = x[1] - x[0]
    
    # 1.
    one = [None] * n
    for i in range(n):
        if i == 0:
            one[i] = right_diff(y[i], y[i+1], h)
        else:
            one[i] = left_diff(y[i-1], y[i], h)
            
    # 2.
    central = [None] * n
    for i in range(1, n - 1):
        central[i] = central_diff(y[i-1], y[i+1], 2 * h)
        
    # 3.
    runge = [None] * n
    for i in range(n):
        if i <= n - 3:
            runge[i] = runge_right_diff(y[i], y[i+1], y[i+2], h)
        else:
            runge[i] = runge_left_diff(y[i-2], y[i-1], y[i], h)
            
    # 4.
    aligned = aligned_diff(x, y)
    
    # 5.
    second = [None] * n
    for i in range(1, n - 1):
        second[i] = second_diff(y[i-1], y[i], y[i+1], h)
        
    print("+" + ("-" * 13 + "+" ) * 7)
    print(f"| {'x':^11} | {'y':^11} | {'1':^11} | {'2':^11} | {'3':^11} | {'4':^11} | {'5':^11} |")
    print("+" + ("-" * 13 + "+" ) * 7)
    for i in range(n):
        print(f"| {x[i]:^11} | {y[i]:^11.3f} | {printf(one[i])} | {printf(central[i])} | {printf(runge[i])} | {printf(aligned[i])} | {printf(second[i])} |")
        print("+" + ("-" * 13 + "+" ) * 7)