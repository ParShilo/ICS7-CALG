import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import Patch
from squares import *
from generator import *

class Lab3App:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №3")
        self.root.geometry("1400x850")
        
        self.x_data, self.y_data, self.rho_vars = [], [], []
        self.x2_data, self.y2_data, self.z2_data, self.rho2_vars = [], [], [], []
        self.setup_notebook()

    def setup_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="1. Одномерная аппроксимация")
        self.setup_tab1()

        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="2. Двумерная аппроксимация")
        self.setup_tab2()

        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="3. Выбор оптимальной функции")
        self.setup_tab3()

        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="4. Краевая задача")
        ttk.Label(self.tab4, text="В разработке").pack(expand=True)

#-----------------------------------------------------------------------------
    def setup_tab1(self):
        self.pane1 = ttk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        self.pane1.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(self.pane1, width=450)
        self.pane1.add(left_frame, weight=1)
        right_frame = ttk.Frame(self.pane1, width=650)
        self.pane1.add(right_frame, weight=2)

        self.setup_controls_1d(left_frame)
        self.setup_plot_1d(right_frame)

    def setup_controls_1d(self, frame):
        ctrl_frame = ttk.LabelFrame(frame, text="Параметры генерации")
        ctrl_frame.pack(fill=tk.X, padx=5, pady=5)

        row1 = ttk.Frame(ctrl_frame)
        row1.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row1, text="N точек:").pack(side=tk.LEFT)
        self.entry_N = ttk.Entry(row1, width=5)
        self.entry_N.insert(0, "10")
        self.entry_N.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="Степень n:").pack(side=tk.LEFT)
        self.entry_n = ttk.Entry(row1, width=5)
        self.entry_n.insert(0, "1")
        self.entry_n.pack(side=tk.LEFT, padx=5)

        ttk.Button(ctrl_frame, text="Сгенерировать данные", command=self.generate_and_display).pack(fill=tk.X, padx=5, pady=2)

        plot_frame = ttk.LabelFrame(frame, text="Построение аппроксимации")
        plot_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(plot_frame, text="Построить (заданное n)", command=lambda: self.plot_results(mode='n')).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(plot_frame, text="Сравнить веса (ρ=1 vs Изм.)", command=lambda: self.plot_results(mode='weights')).pack(fill=tk.X, padx=5, pady=2)

        self.table_canvas_1d = tk.Canvas(frame)
        self.scroll_1d = ttk.Scrollbar(frame, orient="vertical", command=self.table_canvas_1d.yview)
        self.scrollable_frame_1d = ttk.Frame(self.table_canvas_1d)
        self.scrollable_frame_1d.bind("<Configure>", lambda e: self.table_canvas_1d.configure(scrollregion=self.table_canvas_1d.bbox("all")))
        self.table_canvas_1d.create_window((0, 0), window=self.scrollable_frame_1d, anchor="nw")
        self.table_canvas_1d.configure(yscrollcommand=self.scroll_1d.set)
        self.table_canvas_1d.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_1d.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_plot_1d(self, frame):
        self.fig1, self.ax1 = plt.subplots(figsize=(7, 6))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=frame)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        NavigationToolbar2Tk(self.canvas1, frame)

    def generate_and_display(self):
        try:
            N = int(self.entry_N.get())
            if N < 2: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "N должно быть целым числом >= 2")
            return

        self.x_data.clear()
        self.y_data.clear()
        self.rho_vars.clear()
        for widget in self.scrollable_frame_1d.winfo_children():
            widget.destroy()

        x_new, y_new, rho_new = generate_data(N)

        for i in range(N):
            self.x_data.append(x_new[i])
            self.y_data.append(y_new[i])

            row = ttk.Frame(self.scrollable_frame_1d)
            row.pack(fill=tk.X, padx=2, pady=1)
            ttk.Label(row, text=f"{i+1}", width=10, anchor="w").pack(side=tk.LEFT, padx=2)
            ttk.Label(row, text=f"x={x_new[i]:.2f}", width=10, anchor="w").pack(side=tk.LEFT, padx=2)
            ttk.Label(row, text=f"y={y_new[i]:.2f}", width=10, anchor="w").pack(side=tk.LEFT, padx=2)

            rho_var = tk.DoubleVar(value=rho_new[i])
            self.rho_vars.append(rho_var)
            ttk.Entry(row, textvariable=rho_var, width=8).pack(side=tk.LEFT, padx=2)

    def plot_results(self, mode='n'):
        if not self.x_data:
            messagebox.showwarning("Внимание", "Сначала сгенерируйте данные.")
            return

        rho_user = [v.get() for v in self.rho_vars]
        x = self.x_data
        y = self.y_data

        self.ax1.clear()
        self.ax1.scatter(x, y, color='black', zorder=5, label='Исходные точки', s=30)

        if mode == 'n':
            rho_eq = [1.0] * len(x)

            try:
                n = int(self.entry_n.get())
            except ValueError:
                messagebox.showerror("Ошибка", "n должно быть целым числом")
                return
            
            rho = least_squares(x, y, rho_eq, n)
            self._draw_line_1d(rho, f"n={n}, ρ=1", color='grey')

            coeffs = least_squares(x, y, rho_user, n)
            self._draw_line_1d(coeffs, f"n={n}, ρ из таблицы", color='black')

        elif mode == 'weights':
            rho_eq = [1.0] * len(x)

            try:
                n = int(self.entry_n.get())
            except ValueError:
                messagebox.showerror("Ошибка", "n должно быть целым числом")
                return

            n1 = least_squares(x, y, rho_eq, 1)
            self._draw_line_1d(n1, "n=1 ρ=1", color='grey', style='-')

            n2 = least_squares(x, y, rho_eq, 2)
            self._draw_line_1d(n2, "n=2 ρ=1", color='grey', style='--')

            n1_user = least_squares(x, y, rho_user, n)
            self._draw_line_1d(n1_user, "ρ из таблицы", color='black', style='-')

        self.ax1.legend(fontsize=9)
        self.ax1.grid(True, alpha=0.3)
        self.ax1.set_title("Результаты аппроксимации МНК")
        self.ax1.set_xlabel("x")
        self.ax1.set_ylabel("y")
        self.canvas1.draw()

    def _draw_line_1d(self, coeffs, label, color='black', style='-'):
        xmin = min(self.x_data)
        xmax = max(self.x_data)
        x_plot = [xmin + i * (xmax - xmin) / 200 for i in range(201)]
        y_plot = evaluate_polynomial(coeffs, x_plot)
        self.ax1.plot(x_plot, y_plot, linestyle=style, linewidth=2, color=color, label=label)

#-----------------------------------------------------------------------------
    def setup_tab2(self):
        self.pane2 = ttk.PanedWindow(self.tab2, orient=tk.HORIZONTAL)
        self.pane2.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(self.pane2, width=450)
        self.pane2.add(left_frame, weight=1)
        right_frame = ttk.Frame(self.pane2, width=650)
        self.pane2.add(right_frame, weight=2)

        self.setup_controls_2d(left_frame)
        self.setup_plot_2d(right_frame)

    def setup_controls_2d(self, frame):
        ctrl_frame = ttk.LabelFrame(frame, text="Параметры генерации 2D")
        ctrl_frame.pack(fill=tk.X, padx=5, pady=5)

        row1 = ttk.Frame(ctrl_frame)
        row1.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row1, text="N точек:").pack(side=tk.LEFT)
        self.entry_N2 = ttk.Entry(row1, width=5)
        self.entry_N2.insert(0, "50")
        self.entry_N2.pack(side=tk.LEFT, padx=5)

        ttk.Button(ctrl_frame, text="Сгенерировать 2D данные", command=self.generate_and_display_2d).pack(fill=tk.X, padx=5, pady=2)

        plot_frame = ttk.LabelFrame(frame, text="Построение поверхностей")
        plot_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(plot_frame, text="Построить (ρ=1, n=1 и 2)", command=lambda: self.plot_2d_results(mode='both')).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(plot_frame, text="Сравнить веса (n=1)", command=lambda: self.plot_2d_results(mode='weights')).pack(fill=tk.X, padx=5, pady=2)

        self.table_canvas_2d = tk.Canvas(frame)
        self.scroll_2d = ttk.Scrollbar(frame, orient="vertical", command=self.table_canvas_2d.yview)
        self.scrollable_frame_2d = ttk.Frame(self.table_canvas_2d)
        self.scrollable_frame_2d.bind("<Configure>", lambda e: self.table_canvas_2d.configure(scrollregion=self.table_canvas_2d.bbox("all")))
        self.table_canvas_2d.create_window((0, 0), window=self.scrollable_frame_2d, anchor="nw")
        self.table_canvas_2d.configure(yscrollcommand=self.scroll_2d.set)
        self.table_canvas_2d.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_2d.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_plot_2d(self, frame):
        self.fig2, self.ax2 = plt.subplots(figsize=(7, 6), subplot_kw={'projection': '3d'})
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=frame)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        NavigationToolbar2Tk(self.canvas2, frame)

    def generate_and_display_2d(self):
        try:
            N = int(self.entry_N2.get())
            if N < 4: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "N должно быть целым числом >= 4")
            return

        self.x2_data.clear()
        self.y2_data.clear()
        self.z2_data.clear()
        self.rho2_vars.clear()
        for w in self.scrollable_frame_2d.winfo_children(): w.destroy()

        x_new, y_new, z_new, rho_new = generate_data_2d(N)
        for i in range(N):
            self.x2_data.append(x_new[i])
            self.y2_data.append(y_new[i])
            self.z2_data.append(z_new[i])

            row = ttk.Frame(self.scrollable_frame_2d)
            row.pack(fill=tk.X, padx=2, pady=1)
            ttk.Label(row, text=f"{i+1}", width=10, anchor="w").pack(side=tk.LEFT, padx=2)
            ttk.Label(row, text=f"x={x_new[i]:.2f}", width=10, anchor="w").pack(side=tk.LEFT, padx=2)
            ttk.Label(row, text=f"y={y_new[i]:.2f}", width=10, anchor="w").pack(side=tk.LEFT, padx=2)
            ttk.Label(row, text=f"z={z_new[i]:.2f}", width=10, anchor="w").pack(side=tk.LEFT, padx=2)

            v = tk.DoubleVar(value=rho_new[i])
            self.rho2_vars.append(v)
            ttk.Entry(row, textvariable=v, width=8).pack(side=tk.LEFT, padx=2)

    def plot_2d_results(self, mode='both'):
        if not self.x2_data:
            messagebox.showwarning("Внимание", "Сначала сгенерируйте 2D данные.")
            return

        self.ax2.clear()
        x, y, z = self.x2_data, self.y2_data, self.z2_data
        rho_user = [v.get() for v in self.rho2_vars]
        rho_eq = [1.0]*len(x)

        xmin, xmax = min(x), max(x)
        ymin, ymax = min(y), max(y)
        Xg, Yg = np.meshgrid(np.linspace(xmin, xmax, 50), np.linspace(ymin, ymax, 50))

        self.ax2.scatter(x, y, z, color='black', s=20, zorder=5)

        handles = [Patch(color='black', label='Исходные точки')]

        if mode == 'both':
            c1, b1 = least_squares_2d(x, y, z, rho_eq, 1)
            Z1 = np.array([[evaluate_polynomial_2d(c1, b1, xi, yi) for xi in Xg[0]] for yi in Yg[:,0]])
            self.ax2.plot_surface(Xg, Yg, Z1, alpha=0.6, color='red')
            handles.append(Patch(color='red', alpha=0.6, label='n=1, ρ=1'))

            c2, b2 = least_squares_2d(x, y, z, rho_eq, 2)
            Z2 = np.array([[evaluate_polynomial_2d(c2, b2, xi, yi) for xi in Xg[0]] for yi in Yg[:,0]])
            self.ax2.plot_surface(Xg, Yg, Z2, alpha=0.5, color='blue')
            handles.append(Patch(color='blue', alpha=0.5, label='n=2, ρ=1'))
            
        elif mode == 'weights':
            c1, b1 = least_squares_2d(x, y, z, rho_eq, 1)
            Z1 = np.array([[evaluate_polynomial_2d(c1, b1, xi, yi) for xi in Xg[0]] for yi in Yg[:,0]])
            self.ax2.plot_surface(Xg, Yg, Z1, alpha=0.7, color='red')
            handles.append(Patch(color='red', alpha=0.7, label='n=1, ρ=1'))

            c1_u, b1_u = least_squares_2d(x, y, z, rho_user, 1)
            Z1_u = np.array([[evaluate_polynomial_2d(c1_u, b1_u, xi, yi) for xi in Xg[0]] for yi in Yg[:,0]])
            self.ax2.plot_surface(Xg, Yg, Z1_u, alpha=0.7, color='green')
            handles.append(Patch(color='green', alpha=0.7, label='n=1, ρ из таблицы'))

        self.ax2.set_xlabel('X')
        self.ax2.set_ylabel('Y')
        self.ax2.set_zlabel('Z')
        
        self.ax2.legend(handles=handles)
        self.ax2.set_title("2D Аппроксимация МНК")
        self.canvas2.draw()

#-------------------------------------------------------------
    def setup_tab3(self):
        pane = ttk.PanedWindow(self.tab3, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(pane, width=400)
        pane.add(left_frame, weight=1)

        right_frame = ttk.Frame(pane)
        pane.add(right_frame, weight=2)

        ttk.Button(left_frame, text="Вычислить и сравнить", command=self.run_task3).pack(pady=10)

        self.result_text = tk.Text(left_frame, height=25, width=45)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.fig3, self.ax3 = plt.subplots(figsize=(7,6))
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=right_frame)
        self.canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        NavigationToolbar2Tk(self.canvas3, right_frame)

    def run_task3(self):
        x = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        y = [10.5, 1.6, 0.55, 0.26, 0.15, 0.08]

        self.ax3.clear()
        self.ax3.scatter(x, y, color='black', label='Данные')
        self.result_text.delete("1.0", tk.END)

        results = {}

        # 1. Степенная
        a1, b1 = fit_power(x, y)
        y1 = eval_power(x, a1, b1)
        rms1 = compute_rms(y, y1)
        results["a * x^b"] = rms1
        self.ax3.plot(x, y1, label="a * x^b")

        # 2. Экспонента
        a2, b2 = fit_exponential(x, y)
        y2 = eval_exponential(x, a2, b2)
        rms2 = compute_rms(y, y2)
        results["a * e^(bx)"] = rms2
        self.ax3.plot(x, y2, label="a * e^(bx)")

        # 3. Гипербола
        a3, b3 = fit_fraction(x, y)
        y3 = eval_fraction(x, a3, b3)
        rms3 = compute_rms(y, y3)
        results["a + b/x"] = rms3
        self.ax3.plot(x, y3, label="a + b/x")

        # 4. Рациональная
        a0, a1_r, a2_r = fit_rational(x, y)
        y4 = eval_rational(x, a0, a1_r, a2_r)
        rms4 = compute_rms(y, y4)
        results["a0/(a1+a2x)"] = rms4
        self.ax3.plot(x, y4, label="a0/(a1+a2x)")

        best = min(results, key=results.get)

        self.result_text.insert(tk.END, "Результаты аппроксимации:\n\n")

        self.result_text.insert(tk.END,
            f"1) y = a * x^b\n"
            f"   a = {a1:.6f}\n"
            f"   b = {b1:.6f}\n"
            f"   RMS = {rms1:.6f}\n\n")

        self.result_text.insert(tk.END,
            f"2) y = a * e^(b x)\n"
            f"   a = {a2:.6f}\n"
            f"   b = {b2:.6f}\n"
            f"   RMS = {rms2:.6f}\n\n")

        self.result_text.insert(tk.END,
            f"3) y = a + b/x\n"
            f"   a = {a3:.6f}\n"
            f"   b = {b3:.6f}\n"
            f"   RMS = {rms3:.6f}\n\n")

        self.result_text.insert(tk.END,
            f"4) y = a0/(a1 + a2 x)\n"
            f"   a0 = {a0:.6f}\n"
            f"   a1 = {a1_r:.6f}\n"
            f"   a2 = {a2_r:.6f}\n"
            f"   RMS = {rms4:.6f}\n\n")

        self.result_text.insert(tk.END,
            f"Лучшая модель: {best}\n")

        self.ax3.set_title("Сравнение моделей")
        self.ax3.legend()
        self.ax3.grid(True)
        self.canvas3.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = Lab3App(root)
    root.mainloop()