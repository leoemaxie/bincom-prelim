def sum_fibanocci_sequence():
    """Finds the sum of the first 50 fibanocci sequence"""
    a, b, sum = 0, 1, 0

    for i in range(50):
        sum += a
        a = b
        b = a + b

    return sum

if __name__ == '__main__':
    print(sum_fibanocci_sequence())