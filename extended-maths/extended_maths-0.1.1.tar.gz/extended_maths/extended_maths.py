# Module: Extended Maths
# Author: Harsh Gupta <harshgupta204016@gmail.com>
# License: MIT
# Release: Extended maths


def factorial(number):
    """
    A function to calculate factorial of a number.
    
    param number: integer
    """
    if number is None or not isinstance(number , int):
        raise Exception("Entered number must be of type 'int' ")
    if number == 0:
        return 1
    result=1
    #added for the small numbers
    if number < pow(2,20):
        for iter in range(2,number+1):
            result = result*iter
            
    return result

def isPalindrome(number):
    """
    A function to check if the string or number is palindrome or not.
    
    param number: string or intger
    """
    if isinstance(number , int):
        number = str(number)
    return number == number[::-1]

def isSquare(number):
    """
    A function to check if the number is a square of a number.

    param number: intger
    
    returns Boolean value True or False
    """

    if not isinstance(number , int):
        raise Exception("Entered number must be of type 'int' ")

    expected_number = number**0.5
    return True if expected_number%1==0 else False 


def toKelvin(temp):
    """
    A function to convert given celsius temperature to kelvin.

    param temp: intger or float
    
    returns kelvin temperature
    """

    kelvin = 273.15 + temp
    return kelvin

def toFahrenheit(temp):
    """
    A function to convert given celsius temperature to fahrenheit.

    param number: intger or float
    
    returns fahrenheit temperature
    """

    fahrenheit = 1.8 * temp + 32
    return fahrenheit
