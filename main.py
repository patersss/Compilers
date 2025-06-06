from cTreeParser import *
from semantic_analyzer import SemanticAnalyzer
import os
import sys
from ast_visualizer import visualize_ast

def print_tree(ast):
    print("\nАбстрактное синтаксическое дерево:")
    print(*ast, sep=os.linesep)

def analyze_code(code: str) -> None:
    try:
        # Строим AST
        ast = build_tree(code)
        visualize_ast(ast)
        
        # Создаем анализатор и проверяем семантику
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(ast)
        
        # Выводим ошибки, если они есть
        if errors:
            print("\nНайдены семантические ошибки:")
            for error in errors:
                print(f"- {error}")
        else:
            print("\nСемантических ошибок не найдено")
            
    except Exception as e:
        print(f"Ошибка при анализе кода: {e}")

def read_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)

# Тестовые примеры
EXAMPLES = {
    "1": {
        "name": "Дублирование глобальных переменных",
        "code": '''
        int main() {
            int a = 5;
            int b = 10;
            int a = 20;  // Ошибка: повторное объявление глобальной переменной a
        }
        '''
    },
    "2": {
        "name": "Пересечение глобальных и локальных переменных",
        "code": '''
            int main() {
                int x = 10;  // OK: локальная переменная x
                return x;
            }
            x = 20;  // OK: глобальная переменная x
        '''
    },
    "3": {
        "name": "Переменные в циклах",
        "code": '''
            int main() {
                for (int i = 0; i < 5; i++) {
                    int temp = i * 2;
                }
                temp = 10;  // Ошибка: temp не видна вне цикла
                return 0;
            }
        '''
    },
    "4": {
        "name": "Локальные переменные в функциях",
        "code": '''
            int global_var = 5;
            
            int func1() {
                int local_var = 10;
                return local_var;
            }
            
            int main() {
                local_var = 20;  // Ошибка: local_var не видна вне функции func1
                return 0;
            }
        '''
    }
}

def print_menu():
    print("\nВыберите способ ввода кода:")
    print("1. Ввести путь к файлу")
    print("2. Выбрать пример из списка")
    print("3. Выйти")
    
    print("\nДоступные примеры:")
    for key, example in EXAMPLES.items():
        print(f"{key}. {example['name']}")

def main():
    while True:
        print_menu()
        choice = input("\nВаш выбор: ").strip()
        
        if choice == "1":
            file_path = input("Введите путь к файлу: ").strip()
            if os.path.exists(file_path):
                code = read_file(file_path)
                analyze_code(code)
            else:
                print("Файл не найден!")
                
        elif choice == "2":
            example_num = input("Введите номер примера: ").strip()
            if example_num in EXAMPLES:
                analyze_code(EXAMPLES[example_num]["code"])
            else:
                print("Неверный номер примера!")
                
        elif choice == "3":
            print("До свидания!")
            break
            
        else:
            print("Неверный выбор!")
        
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main()
