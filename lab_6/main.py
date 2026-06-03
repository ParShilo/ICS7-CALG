from task_1 import *
from task_2 import *

def main():
    while True:
        print("\n\n1. Задание 1")
        print("2. Задание 2")
        print("0. Выход")
        
        choice = input("\nВыберите пункт меню: ").strip()
        
        if choice == "1":
            run_task_1()
        elif choice == "2":
            run_task_2()
        elif choice == "0":
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()