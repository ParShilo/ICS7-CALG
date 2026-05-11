import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from methods import *

def main():
    global eps_entry, iter_entry, result_label
    global x0_entry, y0_entry
    global phi_entry, eps2_entry, iter2_entry, result2_label

    default_font = ("Arial", 16)

    root = tk.Tk()
    root.title("Лабораторная работа №4")
    root.geometry("1000x800")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # ===================== ЗАДАЧА 1 =====================

    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Задача 1")

    system_label = tk.Label(
        tab1,
        text=(
            "Система уравнений:\n\n"
            "1) 20 sin(0.7x + 0.7y) - 7x - 7y = 0\n"
            "2) 20 ln(x) - 6y - x = 0\n\n"
            "Погрешность:\n"
            "ε = √(Δx² + Δy²) / √(x² + y²)"
        ),
        justify="left",
        font=default_font
    )
    system_label.pack(pady=20)

    input_frame = tk.Frame(tab1)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Относительная погрешность ε:", font=default_font)\
        .grid(row=0, column=0, padx=10, pady=10, sticky="e")

    eps_entry = tk.Entry(input_frame, font=default_font, width=15)
    eps_entry.insert(0, "1e-6")
    eps_entry.grid(row=0, column=1, padx=10)

    tk.Label(input_frame, text="Максимум итераций:", font=default_font)\
        .grid(row=1, column=0, padx=10, pady=10, sticky="e")

    iter_entry = tk.Entry(input_frame, font=default_font, width=15)
    iter_entry.insert(0, "50")
    iter_entry.grid(row=1, column=1, padx=10)

    tk.Label(input_frame, text="Начальное приближение x₀:", font=default_font)\
        .grid(row=2, column=0, padx=10, pady=10, sticky="e")

    x0_entry = tk.Entry(input_frame, font=default_font, width=15)
    x0_entry.insert(0, "2.0")
    x0_entry.grid(row=2, column=1, padx=10)

    tk.Label(input_frame, text="Начальное приближение y₀:", font=default_font)\
        .grid(row=3, column=0, padx=10, pady=10, sticky="e")

    y0_entry = tk.Entry(input_frame, font=default_font, width=15)
    y0_entry.insert(0, "1.0")
    y0_entry.grid(row=3, column=1, padx=10)

    tk.Button(tab1, text="Решить", font=default_font, command=solve_task1)\
        .pack(pady=20)

    result_label = tk.Label(tab1, text="", font=default_font, justify="left")
    result_label.pack(pady=20)

    # ===================== ЗАДАЧА 2 =====================

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Задача 2")

    tk.Label(
        tab2,
        text=(
            "Функция Лапласа:\n"
            "Φ(x) = 1/√(2π) ∫₀ˣ exp(-t²/2) dt\n\n"
            "Метод: половинного деления"
        ),
        font=default_font,
        justify="left"
    ).pack(pady=20)

    frame2 = tk.Frame(tab2)
    frame2.pack(pady=10)

    tk.Label(frame2, text="Заданное значение Φ:", font=default_font)\
        .grid(row=0, column=0, padx=10, pady=10, sticky="e")

    phi_entry = tk.Entry(frame2, font=default_font, width=15)
    phi_entry.insert(0, "0.2")
    phi_entry.grid(row=0, column=1, padx=10)

    tk.Label(frame2, text="Относительная погрешность ε:", font=default_font)\
        .grid(row=1, column=0, padx=10, pady=10, sticky="e")

    eps2_entry = tk.Entry(frame2, font=default_font, width=15)
    eps2_entry.insert(0, "1e-6")
    eps2_entry.grid(row=1, column=1, padx=10)

    tk.Label(frame2, text="Максимум итераций:", font=default_font)\
        .grid(row=2, column=0, padx=10, pady=10, sticky="e")

    iter2_entry = tk.Entry(frame2, font=default_font, width=15)
    iter2_entry.insert(0, "100")
    iter2_entry.grid(row=2, column=1, padx=10)

    tk.Button(tab2, text="Решить", font=default_font, command=solve_task2)\
        .pack(pady=20)

    result2_label = tk.Label(tab2, text="", font=default_font)
    result2_label.pack(pady=20)

    # ===================== ЗАДАЧА 3 =====================

    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Задача 3")

    tk.Label(
        tab3,
        text="Задача 3 будет реализована позже.",
        font=default_font
    ).pack(pady=100)

    root.mainloop()


# ===================== SOLVERS =====================

def solve_task1():
    try:
        eps = float(eps_entry.get())
        max_iter = int(iter_entry.get())
        x0 = float(x0_entry.get())
        y0 = float(y0_entry.get())

        if eps <= 0 or max_iter <= 0:
            messagebox.showerror("Ошибка", "Некорректный ввод")
            return

        if x0 <= 0:
            messagebox.showerror("Ошибка", "Начальное приближение должно удовлетворять x > 0")
            return

        x, y, iterations, delta = newton_method(x0, y0, eps, max_iter)

        if x is None:
            result_label.config(text="Ошибка вычислений.")
        else:
            result_label.config(
                text=(
                    f"Найденные корни:\n"
                    f"x = {x:.10f}\n"
                    f"y = {y:.10f}\n\n"
                    f"Число итераций: {iterations}\n"
                    f"Достигнутая относительная погрешность: {delta:.6e}"
                )
            )
    except:
        messagebox.showerror("Ошибка", "Введите корректные значения.")


def solve_task2():
    try:
        phi_val = float(phi_entry.get())
        eps = float(eps2_entry.get())
        max_iter = int(iter2_entry.get())

        x, iterations, error = bisection_method(phi_val, eps, max_iter)

        if x is None:
            result2_label.config(text="Ошибка вычислений.")
        else:
            result2_label.config(
                text=(
                    f"Найдено x = {x:.10f}\n"
                    f"Итераций: {iterations}\n"
                    f"Длина интервала: {error:.2e}"
                )
            )
    except:
        messagebox.showerror("Ошибка", "Некорректный ввод")


if __name__ == "__main__":
    main()