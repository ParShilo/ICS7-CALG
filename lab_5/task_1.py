from integral import *

def run_task1():
    f1 = lambda x: abs(x)
    f2 = lambda x: abs(x) ** 2
    a, b = -1, 1
    N_values = [2, 3, 4, 5, 6, 10, 50, 100, 200, 500]
    
    def rel_error(exact, approx):
        return abs(exact - approx) / abs(exact) * 100 if exact != 0 else 0.0
        
    # k = 1
    print("\n\nk = 1   f(x) = |x| Истинное значение: 1.000000")
    print("+" + "-" * 3 + "+" + "-" * 20 + "+" + "-" * 20 + "+" + "-" * 20 + "+")
    print("| N |" + "      Трапеции      " + "|" + "       Симпсон      " + "|" + "      Гаусс (3)     " + "|")
    print("+" + "-" * 3 + "+" + "-" * 20 + "+" + "-" * 20 + "+" + "-" * 20 + "+")
        
    integral_g = gauss3(f1, a, b)
    error_g = rel_error(1.000000, integral_g)
        
    for N in N_values:
        integral_t = trapezoidal(f1, a, b, N)
        error_t = rel_error(1.000000, integral_t)
            
        if N % 2 == 0:
            integral_s = simpson(f1, a, b, N)
            value_s = f"{integral_s:18.12f}"
            error_s = f"{rel_error(1.000000, integral_s):>17.6f}%"
        else:
            value_s, error_s = " ", " "
            
        print(f"|{N:3}| {integral_t:18.12f} | {value_s:18} | {integral_g:18.12f} |")
        print(f"|   | {error_t:>17.6f}% | {error_s:>18} | {error_g:>17.6f}% |")
        print("+" + "-" * 3 + "+" + "-" * 20 + "+" + "-" * 20 + "+" + "-" * 20 + "+")

    # k = 2
    print("\n\nk = 2   f(x) = x^2. Истинное значение: 0.666667")
    print("+" + "-" * 3 + "+" + "-" * 20 + "+" + "-" * 20 + "+" + "-" * 20 + "+")
    print("| N |" + "      Трапеции      " + "|" + "       Симпсон      " + "|" + "      Гаусс (3)     " + "|")
    print("+" + "-" * 3 + "+" + "-" * 20 + "+" + "-" * 20 + "+" + "-" * 20 + "+")
        
    integral_g = gauss3(f2, a, b)
    error_g = rel_error(2/3, integral_g)
        
    for N in N_values:
        integral_t = trapezoidal(f2, a, b, N)
        error_t = rel_error(2/3, integral_t)
            
        if N % 2 == 0:
            integral_s = simpson(f2, a, b, N)
            value_s = f"{integral_s:18.12f}"
            error_s = f"{rel_error(2/3, integral_s):>17.6f}%"
        else:
            value_s, error_s = " ", " "
            
        print(f"|{N:3}| {integral_t:18.12f} | {value_s:18} | {integral_g:18.12f} |")
        print(f"|   | {error_t:>17.6f}% | {error_s:>18} | {error_g:>17.6f}% |")
        print("+" + "-" * 3 + "+" + "-" * 20 + "+" + "-" * 20 + "+" + "-" * 20 + "+")
