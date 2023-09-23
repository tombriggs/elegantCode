def sum_of_multiples_3_or_5(num):
    total = 0
    for i in range(3,num):
        if i % 3 == 0 or i % 5 == 0:
            print(i)
            total += i
    return total


print(sum_of_multiples_3_or_5(1000))
