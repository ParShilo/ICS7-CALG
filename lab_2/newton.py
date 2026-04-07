import math

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


def newton_interpolation_1d(table, target_x, n):
    n = min(n, len(table) - 1)
    points = get_points(table, target_x, n + 1)
    coefs = [points[0][1]]
    
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
    
    result = 0.0
    product = 1.0
    for i in range(len(coefs)):
        result += coefs[i] * product
        if i < len(points) - 1:
            product *= (target_x - points[i][0])
    
    return result