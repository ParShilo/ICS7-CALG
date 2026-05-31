import math

def trapezoidal(f, a, b, N):
    h = (b - a) / N
    I = (f(a) + f(b)) / 2.0
    for i in range(1, N):
        I += f(a + i * h)
    return I * h

def simpson(f, a, b, N):
    if N % 2 != 0:
        return None
    h = (b - a) / N
    I = f(a) + f(b)
    for i in range(1, N):
        coeff = 4.0 if i % 2 == 1 else 2.0
        I += coeff * f(a + i * h)
    return I * h / 3.0

def gauss3(f, a, b):
    weights = (5.0/9.0, 8.0/9.0, 5.0/9.0)
    nodes = (-math.sqrt(3.0/5.0), 0.0, math.sqrt(3.0/5.0))
    
    half_len = (b - a) / 2.0
    center = (a + b) / 2.0
    
    I = 0.0
    for i in range(3):
        x = half_len * nodes[i] + center
        I += weights[i] * f(x)
    return I * half_len