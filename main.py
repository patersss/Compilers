from cTreeParser import *
import os

s = '''
        bool a = true;
        int b ;
        /* comment 1
        cin >> c
        */

        cin >> a;
        b = a + a * 10;;

        for (int i = 0; i < 5; i = i + 2)
            cout << b;

        while (true){
            if (a > b + 1 & x) {
                cout << b;  // comment 2
                a = 0;
            }
            else
                if (8 > 9)
                    cout << a;
                else {
                    a=9;}

            a = 90;
        }

        do{
            cout << a - b;
            a = a - b;
        } while (!a != (1 + 9) * b / 8);

    '''

s1 = '''int a = -(2 + 1);
        cin >> a;

        {
            if (a==5)
                { }
            int l = 90;
        }

        int l =97;
        ;;;;
         '''

print(*build_tree(s), sep=os.linesep)
