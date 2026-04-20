from data_reading import load_table
from interpolator import interpolate_3d, interpolate_mixed

def format_result(value, precision=6):
    return f"{value:.{precision}f}"

def validate_point(target, coords):
    x_vals, y_vals, z_vals = coords
    x, y, z = target
    return (min(x_vals) <= x <= max(x_vals) and
            min(y_vals) <= y <= max(y_vals) and
            min(z_vals) <= z <= max(z_vals))

def print_menu():
    print("\n+------------------------------------+")
    print("| 1. Интерполяция полиномами Ньютона |")
    print("| 2. Интерполяция сплайнами          |")
    print("| 3. Смешанная интерполяция          |")
    print("| 0. Выход                           |")
    print("+------------------------------------+")


def get_method_choice():
    while True:
        print_menu()
        choice = input("Выберите метод (0-3): ").strip()
        if choice in '0123':
            return choice
        print("Неверный ввод. Попробуйте снова.")


def get_point_input(coords):
    x_vals, y_vals, z_vals = coords
    print(f"\n\n            Введите нужную точку    "
          f"\n+--------------------------------------------+"
          f"\n| Диапазоны: x ∈ [{x_vals[0]},{x_vals[-1]}], y ∈ [{y_vals[0]},{y_vals[-1]}], z ∈ [{z_vals[0]},{z_vals[-1]}] |"
          f"\n+--------------------------------------------+")

    
    x = float(input("x = ").strip())
    y = float(input("y = ").strip())
    z = float(input("z = ").strip())
    return (x, y, z)

def get_degree_input():
    n = int(input("Степень полинома (0-4): ").strip())
    return max(0, min(4, n))

def main():
    filepath = 'data.txt'
    table_3d, coords = load_table(filepath)
        
    while True:
        choice = get_method_choice()
        if choice == '0':
            print("Завершение работы.")
            break
        
        target = get_point_input(coords)
        if not target or not validate_point(target, coords):
            print("Точка вне диапазона таблицы.")
        
        if choice == '1':
            degree = get_degree_input()
            result = interpolate_3d(table_3d, coords, *target, method_x='newton', method_y='newton', method_z='newton', degree_x=degree, degree_y=degree, degree_z=degree)
            print(f"\nРезультат (Ньютон, степень {degree}): {format_result(result)}")
        
        elif choice == '2':
            result = interpolate_3d(table_3d, coords, *target, method_x='spline', method_y='spline', method_z='spline')
            print(f"\nРезультат (сплайн): {format_result(result)}")
        
        elif choice == '3':
            axis = input("По какой оси использовать сплайн? (x/y/z): ").strip().lower()
            axis_map = {'x': 0, 'y': 1, 'z': 2}
            if axis not in axis_map:
                print("Неверная ось. Используется сплайн по X.")
                spline_axis = 0
            else:
                spline_axis = axis_map[axis]
            
            degree = get_degree_input()
            Mixedresult = interpolate_mixed(table_3d, coords, target, spline_axis=spline_axis, degree=degree)
            axes = ['x', 'y', 'z']
            print(f"\nРезультат (смешанный: сплайн по {axes[spline_axis]}, "
                  f"Ньютон по остальным, степень {degree}): {format_result(Mixedresult)}")

if __name__ == '__main__':
    main()