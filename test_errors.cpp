int processValues(int x, char c, bool b) {
    // Ошибки в бинарных операциях
    int result1 = x + 'A';      // можем складывать int и char
    char result2 = c + true;    // Ошибка: char + bool
    bool result3 = b + 5;       // Ошибка: bool + int
    
    // Ошибки в присваиваниях
    int num = 'A';              // Ошибка: int = char
    char ch = 65;               // Ошибка: char = int
    bool flag = 5;              // Ошибка: bool = int
    
    return result1;
}

// Функция с ошибками в условных операторах
void checkConditions(int x, char c) {
    // Ошибки в if
    if (x > 'A') {              // Ошибка: сравнение int и char
        int local = x;
    }
    
    // Ошибки в while
    while (x > true) {          // Ошибка: сравнение int и bool
        x = x - 1;
    }
    
    // Ошибки в for
    for (int i = 0; i < 'A'; i++) { // Ошибка: сравнение int и char
        int aa = 'a' + i;
    }
}

int main() {
    // Ошибки в объявлении переменных
    int x = 'A';                // Ошибка: int = char
    char c = 65;                // Ошибка: char = int
    bool b = 5;                 // Ошибка: bool = int
    
    // Ошибки в вызовах функций
    int result = processValues('A', 65, 5);  // Ошибка: несоответствие типов
    checkConditions(true, 'A');             // Ошибка: несоответствие типов
    
    return 0;
} 