from reading import read_data
from interpolation import newton_polynomial2D
from simpson import simpson_integral, simpson_integral_by_N
from gauss import gauss_integral, gauss_integral_by_N

def run_task2():
    eps = 1e-5
    degree = 3

    try:
        alpha = float(input("Введите α (по умолч. 1): ") or 1.0)
        beta  = float(input("Введите β (по умолч. 4): ") or 4.0)
        a_val = float(input("Введите a (по умолч. 0): ") or 0.0)
        b_val = float(input("Введите b (по умолч. 2): ") or 2.0)

    except ValueError:
        alpha, beta, a_val, b_val = 1.0, 4.0, 0.0, 2.0

    try:
        data = read_data("data.txt")
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return

    x_unique = sorted(list(set(p[0] for p in data)))
    y_unique = sorted(list(set(p[1] for p in data)))

    Z = {}
    for x, y, z in data:
        Z.setdefault(x, {})[y] = z

    f = lambda x, y: newton_polynomial2D(Z, x_unique, y_unique, x, y, 2)
    phi = lambda x: alpha * x**2
    psi = lambda x: beta  * x**2

    print(f"x∈[{a_val}, {b_val}], y∈[{alpha}*x², {beta}*x²]\n")

    print("Симпсон (внутр.) + Гаусс (внешн.)")
    I_SG = gauss_integral(lambda x: simpson_integral(lambda y: f(x,y), phi(x), psi(x), eps), a_val, b_val, degree, eps)
    print("Гаусс (внутр.) + Симпсон (внешн.)")
    I_GS = simpson_integral(lambda x: gauss_integral(lambda y: f(x,y), phi(x), psi(x), degree, eps), a_val, b_val, eps)
    print("Симпсон (внутр.) + Симпсон (внешн.)")
    I_SS = simpson_integral(lambda x: simpson_integral(lambda y: f(x,y), phi(x), psi(x), eps), a_val, b_val, eps)
    print("Гаусс (внутр.) + Гаусс (внешн.)")
    I_GG = gauss_integral(lambda x: gauss_integral(lambda y: f(x,y), phi(x), psi(x), degree, eps), a_val, b_val, degree, eps)

    print(f"{'Метод':<35} | {'I':>15}")
    print("-" * 55)
    print(f"{'Симпсон (внутр.) + Гаусс (внешн.)':<35} | {I_SG:>15.8f}")
    print(f"{'Гаусс (внутр.) + Симпсон (внешн.)':<35} | {I_GS:>15.8f}")
    print(f"{'Симпсон (внутр.) + Симпсон (внешн.)':<35} | {I_SS:>15.8f}")
    print(f"{'Гаусс (внутр.) + Гаусс (внешн.)':<35} | {I_GG:>15.8f}")

    N = [2, 4, 8, 16, 32, 64]

    methods = [
        ("Simpson -> Simpson", "S", "S", N, N),
        ("Gauss -> Gauss",     "G", "G", N, N),
        ("Simpson -> Gauss",   "S", "G", N, N),
        ("Gauss -> Simpson",   "G", "S", N, N),
    ]

    for name, outer_type, inner_type, N_out, N_in in methods:
        print(f"\n{name}:")
        print("-" * 11 + "+" + ("-" * 12 + "+") * 6)
        print(f"{'N_out\\N_in':>10} | " + " | ".join(f"{n:>10}" for n in N_in))
        print("-" * 11 + "+" + ("-" * 12 + "+") * 6)

        for n_out in N_out:
            row = []
            for n_in in N_in:
                if inner_type == "S":
                    F = lambda x, n=n_in: simpson_integral_by_N(
                        lambda y: f(x, y), phi(x), psi(x), n)
                else:
                    F = lambda x, n=n_in: gauss_integral_by_N(
                        lambda y: f(x, y), phi(x), psi(x), degree, n)

                if outer_type == "S":
                    val = simpson_integral_by_N(F, a_val, b_val, n_out)
                else:
                    val = gauss_integral_by_N(F, a_val, b_val, degree, n_out)

                row.append(f"{val:>10.6f}")
            print(f"{n_out:>10} | " + " | ".join(row))

if __name__ == "__main__":
    run_task2()
