def add_numbers(num1, num2):
    return num1 + num2


def subtract_numbers(num1, num2):
    return num1 - num2


def multiply_numbers(num1, num2):
    return num1 * num2


def divide_numbers(num1, num2):
    return num1 / num2


def factorial_number(num1):
    if num1 == 1:
        return 1
    else:
        return num1 * factorial_number(num1-1)


def palindrome_number(num1):
    r = num1[::-1]
    if r == num1:
        print("Number is palindrom")
    else:
        print("Number is not palindrom")
