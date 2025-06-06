// Простая функция для сложения двух чисел
int add(int a, int b) {
    return a + b;
}

// // Функция для проверки четности числа
bool isEven(int num) {
    return num % 2 == 0;
}


// // Функция с параметрами разных типов
int processValues(int x, char c, bool b) {
    // Проверка бинарных операций
    int result1 = x + 5;        // OK: int + int
    char result2 = c + 1;       // OK: char + int
    
    // Проверка присваиваний
    int num = 10;               // OK: int = int
    char ch = 'A';             // OK: char = char
    bool flag = true;          // OK: bool = bool
    
    // Проверка массивов
    int arr1[5] = {1, 2, 3, 4, 5};     // OK: правильная инициализация
    char arr2[3] = {'a', 'b', 'c'};    // OK: правильная инициализация
    bool arr3[2] = {true, false};      // OK: правильная инициализация
    
    return result1;
}

// // Функция для проверки условных операторов
void checkConditions(int x, char c) {
    // Проверка if
    if (x > 0) {
        int local = x;
    }
    
    // Проверка while
    while (x > 0) {
        x = x - 1;
    }
    
    // Проверка for
    for (int i = 0; i < 5; i++) {
        char ch = 'a' + i;
    }
}

int main() {
    // Объявление переменных
    int x = 10;
    int y = 5;
    char c = 'A';
    bool b = true;
    
    // Работа с массивами
    int numbers[5] = {1, 2, 3, 4, 5};
    char chars[3] = {'a', 'b', 'c'};
    
    // Арифметические операции
    int sum = x + y;
    int diff = x - y;
    int mult = x * y;
    int div = x / y;
    
    // Логические операции
    bool result1 = x > y;
    bool result2 = x == y;
    
    // Условный оператор
    if (x > y) {
        int temp = x;
        x = y;
        y = temp;
    }
    
    // Цикл while
    while (x > 0) {
        x = x - 1;
    }
    
    
    
    // Вызов функций
    int total = add(x, y);
    bool even = isEven(x);
    
    // Вызов функций
    int result = processValues(x, c, b);
    checkConditions(x, c);
    
    return 0;
}
