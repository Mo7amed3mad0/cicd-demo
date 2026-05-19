"""
Simple Calculator App
Mohamed Emad - CI/CD Pipeline Demo
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b


def power(base, exp):
    return base ** exp


if __name__ == "__main__":
    print("=== Calculator App ===")
    print(f"add(5, 3)      = {add(5, 3)}")
    print(f"subtract(10,4) = {subtract(10, 4)}")
    print(f"multiply(6, 7) = {multiply(6, 7)}")
    print(f"divide(15, 3)  = {divide(15, 3)}")
    print(f"power(2, 8)    = {power(2, 8)}")
    print("=== All operations completed successfully ===")
