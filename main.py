import math
import re


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
    """ Преобразование инфиксного выражения в обратную польскую нотацию (алгоритм сортировочной станции) """
    OPERATORS = {
        '+': (1, 'L'),
        '-': (1, 'L'),
        '*': (2, 'L'),
        '//': (2, 'L'),
        '%': (2, 'L'),
        '^': (3, 'R')
    }
    FUNCTIONS = {"neg", "sqrt", "sin", "cos", "tan"}

    def tokenize(expr):
        expr = expr.replace('//', ' // ')
        return re.findall(r'\d+\.\d+|\d+|[a-zA-Z_]+|//|%|[+\-*/^()]', expr)

    output = []
    stack = []
    tokens = tokenize(s)

    for token in tokens:
        if re.fullmatch(r'\d+\.\d+|\d+', token):
            output.append(token)
        elif token in FUNCTIONS:
            stack.append(token)
        elif token in OPERATORS:
            while stack and stack[-1] in OPERATORS:
                top = stack[-1]
                if ((OPERATORS[token][1] == 'L' and OPERATORS[token][0] <= OPERATORS[top][0]) or
                        (OPERATORS[token][1] == 'R' and OPERATORS[token][0] < OPERATORS[top][0])):
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Несбалансированные скобки")
            stack.pop()
            if stack and stack[-1] in FUNCTIONS:
                output.append(stack.pop())
        else:
            raise ValueError(f"Неизвестный токен: {token}")

    while stack:
        if stack[-1] in {'(', ')'}:
            raise ValueError("Несбалансированные скобки в конце выражения")
        output.append(stack.pop())

    return ' '.join(output)


def rpn_calculator(ex: str):
    """ RPN калькулятор с вычислением через Stack """
    stack = Stack()
    for token in ex.split():
        if token in {"+", "-", "*", "//", "%", "^"}:

            if stack.size() < 2:
                raise ValueError(f"Недостаточно операндов для бинарной операции: {token}")

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
            elif token == "%":
                result = a % b
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
                stack.push(float(token))
            except ValueError:
                raise ValueError(f"\"{token}\" - неизвестная операция или не число")

    if stack.size() != 1:
        raise ValueError(f"К концу вычислений на стеке оказалось не одно число: {stack.data}")

    result = stack.pop()
    return int(result) if result.is_integer() else result
