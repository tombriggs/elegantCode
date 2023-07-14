/*
Each new term in the Fibonacci sequence is generated by adding the previous two terms. By starting with 1 and 2, the first 10 terms will be:

1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

By considering the terms in the Fibonacci sequence whose values do not exceed four million, find the sum of the even-valued terms.
*/

#include <iostream>

unsigned long long EvenFibonacciNumbers(int range)
{
    unsigned long long sum{0};
    int x{0};
    int y{1};
    int z{0};
    while (x + y < range)
    {
        z = x + y;
        x = y;
        y = z;
        if (z % 2 == 0) sum = sum + z;
    }
    return sum;
}

int main()
{
    std::cout << EvenFibonacciNumbers(4000000) << std::endl; //4613732
    return 0;
}