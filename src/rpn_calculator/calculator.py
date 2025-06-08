import math

from .parser import parse_str_infix, is_infix, parse_str_postfix
from .vectors import (parse_vector, vector_abs, is_vector, vector_neg, vector_angle,
                      vector_scalar_mul, vector_sub, vector_add)


class Stack:
    """ Реализация Stack для удобства """

    def __init__(self):
        self.data = []

    def push(self, element):
        self.data.append(element)

    def pop(self):
        if not self.data:
            raise ValueError("Попытка извлечь из пустого стека")
        return self.data.pop()

    def size(self):
        return len(self.data)


def rpn_calculator(ex: str, variables: dict = None):
    """ RPN калькулятор с вычислением через Stack """

    stack = Stack()
    variables = variables or {}

    for token in ex.split():

        # Бинарные операторы
        if token in {"+", "-", "*", "//", "%", "^", "angle"}:
            if stack.size() < 2:
                raise ValueError(f"Недостаточно операндов для оператора: {token}")
            b, a = stack.pop(), stack.pop()

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
                elif not is_vector(a) and not is_vector(b):
                    result = a * b
                else:
                    raise TypeError("Умножение вектора на вектор не поддерживается (используйте angle или dot)")
            elif token == "//":
                if b == 0: raise ZeroDivisionError("Деление на ноль")
                result = a // b
            elif token == "%":
                if b == 0: raise ZeroDivisionError("Деление на ноль по модулю")
                result = a % b
            elif token == "^":
                result = a ** b
            elif token == "angle":
                result = vector_angle(a, b)

            stack.push(result)

        # Унарные операторы
        elif token in {"neg", "sqrt", "sin", "cos", "tan", "abs"}:
            if stack.size() < 1:
                raise ValueError(f"Недостаточно операндов для функции: {token}")
            a = stack.pop()

            result = None
            if token == "neg":
                result = vector_neg(a) if is_vector(a) else -a
            elif token == "abs":
                result = vector_abs(a) if is_vector(a) else abs(a)
            elif is_vector(a):
                raise TypeError(f"Функция {token} не применима к вектору")
            elif token == "sqrt":
                result = math.sqrt(a)
            elif token == "sin":
                result = math.sin(a)
            elif token == "cos":
                result = math.cos(a)
            elif token == "tan":
                result = math.tan(a)

            stack.push(result)

        # Числа, векторы или переменные
        else:
            try:
                val = parse_vector(token)
                stack.push(val)
            except ValueError:
                if token in variables:
                    stack.push(variables[token])
                else:
                    raise ValueError(f"'{token}' - неизвестная переменная или некорректный токен")

    if stack.size() != 1:
        raise ValueError(f"В конце вычислений в стеке осталось более одного элемента: {stack.data}")

    result = stack.pop()
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def evaluate_program(lines: list[str]) -> dict:
    """ Обрабатывает список строк-программ """

    env = {}
    last_result = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        var_name = None
        expression = line
        if '=' in line:
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            expression = parts[1].strip()
            if not var_name.isidentifier():
                raise ValueError(f"Недопустимое имя переменной: {var_name}")

        rpn_expr = parse_str_infix(expression) if is_infix(expression) else parse_str_postfix(expression)

        result = rpn_calculator(rpn_expr, env)

        if var_name:
            env[var_name] = result
        last_result = result

    if last_result is not None and not lines[-1].strip().count('='):
        env['_last'] = last_result

    return env
