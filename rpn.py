import math


class Stack:
    """ Реализация Stack для удобства """
    def __init__(self):
        self.data = []

    def push(self, element):
        self.data.append(element)

    def pop(self):
        return self.data.pop()

    def peek(self):
        return self.data[-1]

    def isEmpty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)


def parse_str_postfix(s: str) -> str:
    """ Чистка строки от лишних пробелов """
    return " ".join(s.strip().split())


def parse_str_infix(s: str) -> str:
    """ Работа с инфиксной записью, пока заглушка """
    raise NotImplementedError("Infix to postfix parsing is not implemented")


def rpn_calculator(ex: str):
    """ RPN калькулятор с вычислением через Stack """
    stack = Stack()
    for token in ex.split():
        if token in {"+", "-", "*", "//", "^"}:

            if stack.size() < 2:
                raise ValueError(f"Недостаточно операндов на Stack: len = {stack.size()}")

            b = stack.pop()
            a = stack.pop()
            result = None

            if token == "+":
                result = a + b
            elif token == "-":
                result = a - b
            elif token == "*":
                result = a * b
            elif token == "//":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = a // b
            elif token == "^":
                result = a ** b

            stack.push(result)

        elif token in {"neg", "sqrt", "sin", "cos", "tan"}:

            if stack.size() < 1:
                raise ValueError(f"Недостаточно операндов для унарной операции: {token}")

            a = stack.pop()
            result = None

            if token == "neg":
                result = -a
            elif token == "sqrt":
                if a < 0:
                    raise ValueError("Квадратный корень из отрицательного числа")
                result = math.sqrt(a)
            elif token == "sin":
                result = math.sin(a)
            elif token == "cos":
                result = math.cos(a)
            elif token == "tan":
                result = math.tan(a)

            stack.push(result)

        else:
            try:
                stack.push(int(token))
            except ValueError:
                raise ValueError(f"\"{token}\" - неизвестная операция или не целое число")

    if stack.size() != 1:
        raise ValueError(f"К концу вычислений на стеке оказалось не одно число: {stack.data}")

    return stack.pop()
