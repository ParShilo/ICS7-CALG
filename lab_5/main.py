import math

def f(x, k):
    return abs(x) ** k

def integrate_trapezoidal(k):
    """Метод трапеций, 3 узла: x = -1, 0, 1. Шаг h = 1"""
    h = 1.0
    return (h / 2.0) * (f(-1, k) + 2 * f(0, k) + f(1, k))

def integrate_simpson(k):
    """Метод Симпсона, 3 узла: x = -1, 0, 1. Шаг h = 1"""
    h = 1.0
    return (h / 3.0) * (f(-1, k) + 4 * f(0, k) + f(1, k))

def integrate_gauss3(k):
    """Квадратура Гаусса, 3 узла на [-1, 1]"""
    # Узлы и веса для 3-точечной формулы Гаусса на [-1, 1]
    x = math.sqrt(3.0 / 5.0)
    w = 5.0 / 9.0
    w_center = 8.0 / 9.0
    
    # В силу симметрии |x|^k: f(-x, k) == f(x, k)
    return w * f(-x, k) + w_center * f(0, k) + w * f(x, k)

def run_task1():
    methods = {
        "Трапеции": integrate_trapezoidal,
        "Симпсон": integrate_simpson,
        "Гаусс (3 узла)": integrate_gauss3
    }

    analytical = [1.0, 2/3]
    
    print("\n" + "-" * 19 + "+" + "-" * 14 + "+" + "-" * 14 + "+" + "-" * 14 + "+" + "-" * 14 + "+")
    print(f"{'Метод':<18} | {'k=1 (числ.)':<12} | {'Погр. k=1':<12} | {'k=2 (числ.)':<12} | {'Погр. k=2':<12} |")
    print("-" * 19 + "+" + "-" * 14 + "+" + "-" * 14 + "+" + "-" * 14 + "+" + "-" * 14 + "+")
    
    for name, func in methods.items():
        res1 = func(1)
        err1 = abs(analytical[0] - res1)
        
        res2 = func(2)
        err2 = abs(analytical[1] - res2)
        
        print(f"{name:<18} | {res1:<12.6f} | {err1:<12.6f} | {res2:<12.6f} | {err2:<12.6f} |")
    print("-" * 19 + "+" + "-" * 14 + "+" + "-" * 14 + "+" + "-" * 14 + "+" + "-" * 14 + "+")

def run_task2():
    print("\n" + "="*60)
    print("ЗАДАНИЕ 2. Двукратный интеграл")
    print("="*60)
    print("⚠️ Функционал в разработке. Здесь будет реализация:")
    print("  • Последовательного интегрирования по Гауссу и Симпсону")
    print("  • Автоматического выбора шага")
    print("  • Вычисления корней полинома Лежандра")
    print("  • Двумерной интерполяции по табличным данным")

def main():
    while True:
        print("\n\n1. Задание 1: Сравнение методов интегрирования")
        print("2. Задание 2: Двукратный интеграл")
        print("0. Выход")
        
        choice = input("\nВыбор: ").strip()
        
        if choice == "1":
            run_task1()
        elif choice == "2":
            run_task2()
        elif choice == "0":
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()