
int add(int a, int b) {
    return a + b;
}

bool isEven(int num) {
    return num % 2 == 0;
}


int processValues(int x, char c, bool b) {
    int result1 = x + 5;        
    int result2 = c + 1;       
    
    int num = 10;               
    char ch = 'A';             
    bool flag = true;          
    
    int arr1[5] = {1, 2, 3, 4, 5};     
    char arr2[3] = {'a', 'b', 'c'};    
    bool arr3[2] = {true, false};      
    
    return result1;
}

void checkConditions(int x, char c) {
    if (x > 0) {
        int local = x;
    }
    
    while (x > 0) {
        x = x - 1;
    }
    
    for (int i = 0; i < 5; i++) {
        int sign= 'a' + i;
    }
}

int main() {
    int x = 10;
    int y = 5;
    char c = 'A';
    bool b = true;
    
    int numbers[5] = {1, 2, 3, 4, 5};
    char chars[3] = {'a', 'b', 'c'};
    
    int sum = x + y;
    int diff = x - y;
    int mult = x * y;
    int div = x / y;
    
    bool result1 = x > y;
    bool result2 = x == y;
    
    if (x > y) {
        int temp = x;
        x = y;
        y = temp;
    }
    
    while (x > 0) {
        x = x - 1;
    }
    
    
    
    int total = add(x, y);
    bool even = isEven(x);
    
    int result = processValues(x, c, b);
    checkConditions(x, c);
    
    return 0;
}
