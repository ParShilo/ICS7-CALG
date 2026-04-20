import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from squares import *
from generator import generate_data

class Lab3App:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №3: МНК")
        self.root.geometry("1300x800")
        
        self.x_data = []
        self.y_data = []
        self.rho_vars = []
        
        self.setup_notebook()

    def setup_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="1. Одномерная аппроксимация")
        
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="2. Двумерная аппроксимация (в разработке)")
        ttk.Label(self.tab2, text="Здесь будет двумерная аппроксимация и графики поверхностей.").pack(expand=True)

        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="3. Выбор оптимальной функции (в разработке)")
        ttk.Label(self.tab3, text="Здесь будет сравнение нелинейных функций.").pack(expand=True)

        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="4. Краевая задача (в разработке)")
        ttk.Label(self.tab4, text="Здесь будет решение ОДУ и графики для m=2,3.").pack(expand=True)

        self.setup_tab1()

    def setup_tab1(self):
        self.pane = ttk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        self.pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(self.pane, width=450)
        self.pane.add(left_frame, weight=1)
        
        right_frame = ttk.Frame(self.pane, width=650)
        self.pane.add(right_frame, weight=2)

        self.setup_controls(left_frame)
        self.setup_plot(right_frame)

    def setup_controls(self, frame):
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

        table_frame = ttk.LabelFrame(frame, text="Таблица данных (двойной клик/ввод для ρ)")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.table_canvas = tk.Canvas(table_frame)
        self.table_scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.table_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.table_canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))
        self.table_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.table_canvas.configure(yscrollcommand=self.table_scrollbar.set)

        self.table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.table_canvas.bind("<Enter>", lambda _: self.table_canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.table_canvas.bind("<Leave>", lambda _: self.table_canvas.unbind_all("<MouseWheel>"))

    def _on_mousewheel(self, event):
        self.table_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def setup_plot(self, frame):
        self.fig, self.ax = plt.subplots(figsize=(7, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack_forget()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def generate_and_display(self):
        try:
            N = int(self.entry_N.get())
            if N < 2:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "N должно быть целым числом >= 2")
            return

        self.x_data.clear()
        self.y_data.clear()
        self.rho_vars.clear()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        x_new, y_new, rho_new = generate_data(N)

        for i in range(N):
            self.x_data.append(x_new[i])
            self.y_data.append(y_new[i])

            row = ttk.Frame(self.scrollable_frame)
            row.pack(fill=tk.X, padx=2, pady=1)

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

        self.ax.clear()
        self.ax.scatter(x, y, color='black', zorder=5, label='Исходные точки', s=30)

        if mode == 'n':
            rho_eq = [1.0] * len(x)

            try:
                n = int(self.entry_n.get())
            except ValueError:
                messagebox.showerror("Ошибка", "n должно быть целым числом")
                return
            
            rho = least_squares(x, y, rho_eq, n)
            self._draw_line(rho, f"n={n}, ρ=1", color='grey')

            coeffs = least_squares(x, y, rho_user, n)
            self._draw_line(coeffs, f"n={n}, ρ из таблицы", color='black')

        elif mode == 'weights':
            rho_eq = [1.0] * len(x)

            try:
                n = int(self.entry_n.get())
            except ValueError:
                messagebox.showerror("Ошибка", "n должно быть целым числом")
                return

            n1 = least_squares(x, y, rho_eq, 1)
            self._draw_line(n1, "n=1 ρ=1", color='grey', style='-')

            n2 = least_squares(x, y, rho_eq, 2)
            self._draw_line(n2, "n=2 ρ=1", color='grey', style='--')

            n1_user = least_squares(x, y, rho_user, n)
            self._draw_line(n1_user, "ρ из таблицы", color='black', style='-')

        self.ax.legend(fontsize=9)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title("Результаты аппроксимации МНК")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.canvas.draw()

    def _draw_line(self, coeffs, label, color='black', style='-'):
        xmin = min(self.x_data)
        xmax = max(self.x_data)
        x_plot = [xmin + i * (xmax - xmin) / 200 for i in range(201)]
        y_plot = evaluate_polynomial(coeffs, x_plot)
        self.ax.plot(x_plot, y_plot, linestyle=style, linewidth=2, color=color, label=label)

if __name__ == "__main__":
    root = tk.Tk()
    app = Lab3App(root)
    root.mainloop()