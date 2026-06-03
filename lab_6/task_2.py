import math
import matplotlib.pyplot as plt

def solve_bvp(alpha, beta, gamma, N=10):
    h = 1.0 / N
    x = [i * h for i in range(N + 1)]
    
    A = [0.0] * (N + 1)
    B = [0.0] * (N + 1)
    C = [0.0] * (N + 1)
    F = [0.0] * (N + 1)
    
    for i in range(N + 1):
        A[i] = 1.0 + h * (x[i] ** 2)
        B[i] = 4.0 * (h ** 2) - 2.0
        C[i] = 1.0 - h * (x[i] ** 2)
        F[i] = (h ** 2) * (2.0 * x[i] + math.exp(-x[i]))
        
    e = [0.0] * (N + 1)
    n = [0.0] * (N + 1)
    
    e[0] = -2.0 / B[0]
    n[0] = (F[0] + 2.0 * h * alpha) / B[0]
    
    for i in range(1, N):
        denom = A[i] * e[i - 1] + B[i]
        e[i] = -C[i] / denom
        n[i] = (F[i] - A[i] * n[i - 1]) / denom
        
    u = [0.0] * (N + 1)

    denom_N = 2.0 * e[N - 1] + B[N] + 2.0 * h * beta * C[N]
    u[N] = (F[N] - 2.0 * h * gamma * C[N] - 2.0 * n[N - 1]) / denom_N
    
    for i in range(N - 1, -1, -1):
        u[i] = e[i] * u[i + 1] + n[i]
        
    return x, u

def run_task_2():
    try:
        print("\n\nu'(0) = alpha.    u'(1) = beta * u(1) + gamma ")
        alpha = float(input("alpha: "))
        beta = float(input("beta : "))
        gamma = float(input("gamma: "))
    except ValueError:
        print("Некорректный ввод. Используются значения по умолчанию: alpha=1, beta=1, gamma=1")
        alpha, beta, gamma = 1.0, 1.0, 1.0
        
    N = 10
    x, u = solve_bvp(alpha, beta, gamma, N)
    
    print("+" + "-" * 5 + "+" + "-" * 12 + "+" + "-" * 20 + "+")
    print(f"| {'i':^3} | {'x_i':^10} | {'u(x_i)':^18} |")
    print("+" + "-" * 5 + "+" + "-" * 12 + "+" + "-" * 20 + "+")
    for i in range(N + 1):
        print(f"| {i:^3} | {x[i]:^10.3f} | {u[i]:^18.8f} |")
        print("+" + "-" * 5 + "+" + "-" * 12 + "+" + "-" * 20 + "+")

    plt.figure(figsize=(8, 5))
    plt.plot(x, u, marker='o', linestyle='-', label=f'u(x), N={N}')
    plt.title('Решение краевой задачи для ОДУ методом прогонки')
    plt.xlabel('x')
    plt.ylabel('u(x)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()