prime_numbers = []
for number in range(2, 1001):
    if any((number % i == 0 for i in range(2, number))):
        pass
    else:
        prime_numbers.append(number)
