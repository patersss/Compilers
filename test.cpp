int main() {
    int x = 5;
    int y = 10;
    
    if (x < y) {
        cout << "x меньше y" << endl;
    } else {
        cout << "x больше или равно y" << endl;
    }
    
    for (int i = 0; i < 5; i++) {
        cout << i << endl;
    }
    
    while (x > 0) {
        x = x - 1;
    }
    
    return 0;
} 