int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

int divide(int a, int b) {
    return a / b;
}

int modulo(int a, int b) {
    return a % b;
}

int main() {
    
    int x = 5;
    char c = 'A';
    bool b = true;
    
    
    int arr[5] = {1, 2, 3, 4, 5};
    char chars[3] = {'a', 'b', 'c'};
    
    
    x = x + 1;
    x = x - 1;
    x = x * 2;
    x = x / 2;
    x = x % 3;
    
    
    if (x > 0) {
        cout << "x is positive" << endl;
    }
    
    if (x >= 5) {
        cout << "x is greater than or equal to 5" << endl;
    }
    
    if (x < 10) {
        cout << "x is less than 10" << endl;
    }
    
    if (x <= 5) {
        cout << "x is less than or equal to 5" << endl;
    }
    
    
    if (x > 0 && x < 10) {
        cout << "x is between 0 and 10" << endl;
    }
    
    if (!b) {
        cout << "b is false" << endl;
    }
    
    
    for (int i = 0; i < 5; i++) {
        cout << arr[i] << endl;
    }
    
    while (x > 0) {
        x = x - 1;
    }
    
    do {
        x = x + 1;
    } while (x < 5);
    
    
    x++;
    x--;
    
    
    x = abs(-5);
    
    
    cin >> x;
    cout << x << endl;
    
    
    int sum = add(5, 3);
    int diff = subtract(10, 4);
    int prod = multiply(6, 7);
    int quot = divide(20, 4);
    int mod = modulo(17, 5);
    
    return 0;
}
