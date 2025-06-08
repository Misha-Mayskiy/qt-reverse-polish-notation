import math
import re

from vectors_rpn import parse_vector, vector_abs, is_vector, vector_neg, vector_angle, vector_scalar_mul, vector_sub, \
    vector_add


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


def is_infix(expr: str) -> bool:
    return bool(re.search(r'[+\-*/^%()]', expr))


def parse_str_postfix(s: str) -> str:
    """ Чистка строки от лишних пробелов """
    return " ".join(s.strip().split())


def parse_str_infix(ex: str) -> str:
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

    def tokenize(expression):
        expression = expression.replace('//', ' // ')
        return re.findall(r'\d+\.\d+|\d+|[a-zA-Z_]+|//|%|[+\-*/^()]', expression)

    output = []
    stack = []
    tokens = tokenize(ex)

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
            output.append(token)

    while stack:
        if stack[-1] in {'(', ')'}:
            raise ValueError("Несбалансированные скобки в конце выражения")
        output.append(stack.pop())

    return ' '.join(output)


def rpn_calculator(ex: str, vars: dict[str, float | list[float]] = None):
    """ RPN калькулятор с вычислением через Stack """
    stack = Stack()
    vars = vars or {}

    for token in ex.split():
        if token in {"+", "-", "*", "//", "%", "^", "angle"}:

            if stack.size() < 2:
                raise ValueError(f"Недостаточно операндов: {token}")

            b = stack.pop()
            a = stack.pop()
            result = None

            if token == "+":
                if is_vector(a) and is_vector(b):
                    result = vector_add(a, b)
                elif not is_vector(a) and not is_vector(b):
                    result = a + b
                else:
                    raise TypeError("Нельзя складывать вектор и скаляр")

            elif token == "-":
                if is_vector(a) and is_vector(b):
                    result = vector_sub(a, b)
                elif not is_vector(a) and not is_vector(b):
                    result = a - b
                else:
                    raise TypeError("Нельзя вычитать вектор и скаляр")
            elif token == "*":
                if is_vector(a) and not is_vector(b):
                    result = vector_scalar_mul(a, b)
                elif not is_vector(a) and is_vector(b):
                    result = vector_scalar_mul(b, a)
                else:
                    result = a * b
            elif token == "//":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = a // b
            elif token == "%":
                result = a % b
            elif token == "^":
                result = a ** b
            elif token == "angle":
                result = vector_angle(a, b)

            stack.push(result)

        elif token in {"neg", "sqrt", "sin", "cos", "tan", "abs"}:

            if stack.size() < 1:
                raise ValueError(f"Недостаточно операндов: {token}")

            a = stack.pop()
            result = None

            if token == "neg":
                result = vector_neg(a) if is_vector(a) else -a
            elif token == "sqrt":
                result = math.sqrt(a)
            elif token == "sin":
                result = math.sin(a)
            elif token == "cos":
                result = math.cos(a)
            elif token == "tan":
                result = math.tan(a)
            elif token == "abs":
                result = vector_abs(a) if is_vector(a) else abs(a)
            stack.push(result)

        else:
            try:
                val = parse_vector(token)
                stack.push(val)
            except ValueError:
                if token in vars:
                    stack.push(vars[token])
                else:
                    raise ValueError(f"\"{token}\" - неизвестный токен")

    if stack.size() != 1:
        raise ValueError(f"Некорректный стек: {stack.data}")

    result = stack.pop()
    return int(result) if isinstance(result, float) and result.is_integer() else result


def evaluate_program(lines: list[str]) -> dict[str, float]:
    """
    Обрабатывает список строк-программ, поддерживает:
    - присваивания: a = 2 3 +
    - вычисления: 4 5 *
    Возвращает финальное состояние переменных.
    """
    env = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if '=' in line:
            varname, ex = map(str.strip, line.split('=', 1))
            if not varname.isidentifier():
                raise ValueError(f"Недопустимое имя переменной: {varname}")

            ex_rpn = parse_str_infix(ex) if is_infix(ex) else parse_str_postfix(ex)
            env[varname] = rpn_calculator(ex_rpn, env)
        else:
            ex_rpn = parse_str_infix(line) if is_infix(line) else parse_str_postfix(line)
            rpn_calculator(ex_rpn, env)

    return env
