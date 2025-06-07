int processValues(int x, char c, bool b) {
    int result1 = x + 'A';      
    char result2 = c + true;    
    bool result3 = b + 5;       
    
    int num = 'A';              
    char ch = 65;               
    bool flag = 5;              
    
    return result1;
}

void checkConditions(int x, char c) {
    if (x > 'A') {              
        int local = x;
    }
    
    while (x > true) {          
        x = x - 1;
    }
    
    for (int i = 0; i < 'A'; i++) { 
        int aa = i + 'a';
    }
}

int check_count_of_params(int x, char c, bool b) {
    return x + c + b;
}

int main() {
    int x = 'A';                
    char c = 65;                
    bool b = 5;
    bool x = true;                 
    int arr[5] = {1, 2, 3, 4, 5, 8};
    char arr2[3] = {'a', 'b', true};
    int dsda = unexisting_function();
    bool dsa = check_count_of_params(1, 2);
    int result = processValues('A', 65, 5);  
    checkConditions(true, 'A');             
    
    return 0;
} 