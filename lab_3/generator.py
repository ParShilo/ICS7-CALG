import random
import math

def generate_data(N):
    x, y, rho = [], [], []
    for i in range(N):
        xi = i * 0.5
        yi = 2 * math.sqrt(xi) - 3 + random.uniform(-2, 2)
        x.append(xi)
        y.append(yi)
        rho.append(1.0)
    return x, y, rho

def generate_data_2d(N):
    x, y, z, rho = [], [], [], []
    for i in range(N):
        xi = random.uniform(0, 10)
        yi = random.uniform(0, 10)
        zi = 2 * math.sqrt(xi) - math.sqrt(yi) + 3 + random.uniform(-2, 2)
        x.append(xi)
        y.append(yi)
        z.append(zi)
        rho.append(1.0)
    return x, y, z, rho