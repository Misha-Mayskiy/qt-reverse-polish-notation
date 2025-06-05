import math
import re


def tokenize(expression):
    """
    Разбивает выражение на токены (числа, операторы, функции, скобки, переменные).
    """
    token_pattern = r'''
        (\d+\.?\d*)|           # числа (целые и вещественные)
        ([a-zA-Z_]\w*)|        # функции, константы и переменные
        (==|!=|<=|>=|<<|>>)|   # двухсимвольные операторы
        ([-+*/^%()])|          # односимвольные операторы и скобки
        (\S)                   # любой другой непробельный символ
    '''

    tokens = []
    for match in re.finditer(token_pattern, expression, re.VERBOSE):
        token = match.group(0)
        if token and not token.isspace():
            tokens.append(token)

    return tokens


def infix_to_rpn(expression, variables=None):
    """
    Преобразует инфиксное выражение в обратную польскую нотацию.

    Args:
        expression (str): Инфиксное арифметическое выражение
        variables (dict): Словарь переменных (для проверки корректности)

    Returns:
        str: Выражение в RPN-нотации
    """
    if variables is None:
        variables = {}

    # Приоритеты операторов
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '//': 2,
        '%': 2,
        '^': 3,
        '**': 3,
        'neg': 4
    }

    # Ассоциативность операторов
    left_associative = {
        '+': True,
        '-': True,
        '*': True,
        '/': True,
        '//': True,
        '%': True,
        '^': False,
        '**': False,
        'neg': False
    }

    # Унарные функции
    unary_functions = {
        'sqrt', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
        'sinh', 'cosh', 'tanh', 'exp', 'ln', 'log', 'abs',
        'floor', 'ceil', 'round', 'rad', 'deg'
    }

    # Константы
    constants = {'pi', 'e'}

    tokens = tokenize(expression)
    output = []
    operator_stack = []

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Проверка на число
        try:
            float(token)
            output.append(token)
        except ValueError:
            # Проверка на константу
            if token.lower() in constants:
                output.append(token.lower())

            # Проверка на переменную
            elif token in variables:
                output.append(f"${token}")  # Помечаем переменные символом $

            # Проверка на функцию
            elif token.lower() in unary_functions:
                operator_stack.append(token.lower())

            # Левая скобка
            elif token == '(':
                operator_stack.append(token)

            # Правая скобка
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Несбалансированные скобки")
                operator_stack.pop()

                if operator_stack and operator_stack[-1] in unary_functions:
                    output.append(operator_stack.pop())

            # Оператор
            elif token in precedence or (
                    token == '-' and (i == 0 or tokens[i - 1] in ['(', '+', '-', '*', '/', '^', '**'])):
                if token == '-' and (i == 0 or tokens[i - 1] in ['(', '+', '-', '*', '/', '^', '**']):
                    operator_stack.append('neg')
                else:
                    while (operator_stack and
                           operator_stack[-1] != '(' and
                           operator_stack[-1] in precedence and
                           (precedence.get(operator_stack[-1], 0) > precedence.get(token, 0) or
                            (precedence.get(operator_stack[-1], 0) == precedence.get(token, 0) and
                             left_associative.get(token, True)))):
                        output.append(operator_stack.pop())
                    operator_stack.append(token)
            else:
                # Предполагаем, что это переменная
                if not token[0].isdigit():
                    output.append(f"${token}")
                else:
                    raise ValueError(f"Неизвестный токен: {token}")

        i += 1

    while operator_stack:
        if operator_stack[-1] in ['(', ')']:
            raise ValueError("Несбалансированные скобки")
        output.append(operator_stack.pop())

    return ' '.join(output)


def calculate_rpn(expression, variables=None):
    """
    Вычисляет выражение в обратной польской нотации с поддержкой переменных.

    Args:
        expression (str): RPN-выражение
        variables (dict): Словарь переменных и их значений

    Returns:
        float: Результат вычисления
    """
    if not expression:
        raise ValueError("Пустое выражение")

    if variables is None:
        variables = {}

    stack = []
    tokens = expression.split()

    # Бинарные операторы
    binary_operators = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
        '//': lambda a, b: a // b,
        '%': lambda a, b: a % b,
        '**': lambda a, b: a ** b,
        '^': lambda a, b: a ** b
    }

    # Унарные операторы
    unary_operators = {
        'neg': lambda x: -x,
        'sqrt': lambda x: math.sqrt(x),
        'sin': lambda x: math.sin(x),
        'cos': lambda x: math.cos(x),
        'tan': lambda x: math.tan(x),
        'asin': lambda x: math.asin(x),
        'acos': lambda x: math.acos(x),
        'atan': lambda x: math.atan(x),
        'sinh': lambda x: math.sinh(x),
        'cosh': lambda x: math.cosh(x),
        'tanh': lambda x: math.tanh(x),
        'exp': lambda x: math.exp(x),
        'ln': lambda x: math.log(x),
        'log': lambda x: math.log10(x),
        'abs': lambda x: abs(x),
        'floor': lambda x: math.floor(x),
        'ceil': lambda x: math.ceil(x),
        'round': lambda x: round(x),
        'rad': lambda x: math.radians(x),
        'deg': lambda x: math.degrees(x)
    }

    for token in tokens:
        if token in binary_operators:
            if len(stack) < 2:
                raise ValueError(f"Недостаточно операндов для операции '{token}'")

            b = stack.pop()
            a = stack.pop()

            if token in ['/', '//', '%'] and b == 0:
                raise ValueError("Деление на ноль")

            result = binary_operators[token](a, b)
            stack.append(result)

        elif token in unary_operators:
            if len(stack) < 1:
                raise ValueError(f"Недостаточно операндов для операции '{token}'")

            a = stack.pop()

            if token == 'sqrt' and a < 0:
                raise ValueError(f"Квадратный корень из отрицательного числа: {a}")
            if token in ['asin', 'acos'] and (a < -1 or a > 1):
                raise ValueError(f"Аргумент {a} вне допустимого диапазона [-1, 1] для {token}")
            if token in ['ln', 'log'] and a <= 0:
                raise ValueError(f"Логарифм неположительного числа: {a}")

            try:
                result = unary_operators[token](a)
                stack.append(result)
            except Exception as e:
                raise ValueError(f"Ошибка при выполнении операции '{token}': {e}")

        else:
            # Проверка на переменную (начинается с $)
            if token.startswith('$'):
                var_name = token[1:]
                if var_name in variables:
                    stack.append(float(variables[var_name]))
                else:
                    raise ValueError(f"Неопределенная переменная: {var_name}")
            else:
                try:
                    number = float(token)
                    stack.append(number)
                except ValueError:
                    if token.lower() == 'pi':
                        stack.append(math.pi)
                    elif token.lower() == 'e':
                        stack.append(math.e)
                    else:
                        raise ValueError(f"Некорректный токен: '{token}'")

    if len(stack) != 1:
        raise ValueError("Некорректное выражение: неверное количество операторов или операндов")

    return stack[0]


def evaluate_expression(expression, variables=None):
    """
    Вычисляет арифметическое выражение с поддержкой переменных.

    Args:
        expression (str): Арифметическое выражение
        variables (dict): Словарь переменных и их значений

    Returns:
        float: Результат вычисления
    """
    rpn = infix_to_rpn(expression, variables)
    return calculate_rpn(rpn, variables)


class Calculator:
    """
    Калькулятор с поддержкой переменных.
    """

    def __init__(self):
        self.variables = {}

    def set_variable(self, name, value):
        """Устанавливает значение переменной."""
        if not name[0].isalpha() and name[0] != '_':
            raise ValueError("Имя переменной должно начинаться с буквы или _")
        if name.lower() in ['pi', 'e', 'sin', 'cos', 'tan', 'sqrt', 'ln', 'log', 'abs']:
            raise ValueError(f"'{name}' является зарезервированным именем")
        self.variables[name] = float(value)

    def get_variable(self, name):
        """Возвращает значение переменной."""
        return self.variables.get(name)

    def delete_variable(self, name):
        """Удаляет переменную."""
        if name in self.variables:
            del self.variables[name]

    def clear_variables(self):
        """Очищает все переменные."""
        self.variables.clear()

    def list_variables(self):
        """Возвращает список всех переменных."""
        return dict(self.variables)

    def evaluate(self, expression):
        """Вычисляет выражение с учетом сохраненных переменных."""
        return evaluate_expression(expression, self.variables)


# Примеры использования
if __name__ == "__main__":
    print("=== Примеры с переменными ===")

    # Простые примеры
    variables = {
        'x': 5,
        'y': 3,
        'radius': 10,
        'angle': 45
    }

    examples = [
        ("x + y", variables),
        ("x * y - 2", variables),
        ("(x + y) / 2", variables),
        ("sqrt(x^2 + y^2)", variables),
        ("pi * radius^2", variables),
        ("sin(angle * pi / 180)", variables),
        ("x * sin(angle * pi / 180) + y * cos(angle * pi / 180)", variables)
    ]

    for expr, vars in examples:
        try:
            rpn = infix_to_rpn(expr, vars)
            result = evaluate_expression(expr, vars)
            print(f"Выражение: {expr}")
            print(f"Переменные: {vars}")
            print(f"RPN: {rpn}")
            print(f"Результат: {result:.6f}")
            print()
        except Exception as e:
            print(f"Ошибка: {e}\n")

    print("\n=== Использование класса Calculator ===")
    calc = Calculator()

    # Установка переменных
    calc.set_variable('a', 10)
    calc.set_variable('b', 20)
    calc.set_variable('c', 30)

    print(f"Переменные: {calc.list_variables()}")

    # Вычисления
    expressions = [
        "a + b + c",
        "a * b / c",
        "sqrt(a^2 + b^2)",
        "(a + b) * c / 2"
    ]

    for expr in expressions:
        result = calc.evaluate(expr)
        print(f"{expr} = {result:.6f}")

    print("\n=== Интерактивный калькулятор с переменными ===")
    print("Команды:")
    print("  <выражение>        - вычислить выражение")
    print("  var = <значение>   - установить переменную")
    print("  vars               - показать все переменные")
    print("  del <var>          - удалить переменную")
    print("  clear              - очистить все переменные")
    print("  exit               - выход")

    calc = Calculator()

    while True:
        try:
            command = input("\n> ").strip()

            if command.lower() == 'exit':
                break
            elif command.lower() == 'vars':
                vars = calc.list_variables()
                if vars:
                    for name, value in vars.items():
                        print(f"  {name} = {value}")
                else:
                    print("  Нет переменных")
            elif command.lower() == 'clear':
                calc.clear_variables()
                print("Все переменные удалены")
            elif command.lower().startswith('del '):
                var_name = command[4:].strip()
                calc.delete_variable(var_name)
                print(f"Переменная '{var_name}' удалена")
            elif '=' in command and not any(op in command for op in ['==', '!=', '<=', '>=']):
                # Присваивание переменной
                parts = command.split('=', 1)
                var_name = parts[0].strip()
                expr = parts[1].strip()
                value = calc.evaluate(expr)
                calc.set_variable(var_name, value)
                print(f"{var_name} = {value}")
            elif command:
                # Вычисление выражения
                result = calc.evaluate(command)
                print(f"= {result}")
        except Exception as e:
            print(f"Ошибка: {e}")

    print("\n=== Дополнительные примеры ===")

    # Пример с физическими формулами
    print("\nФизические формулы:")
    calc = Calculator()

    # Кинематика
    calc.set_variable('v0', 10)  # начальная скорость
    calc.set_variable('a', 9.8)  # ускорение
    calc.set_variable('t', 2)  # время

    print("Движение с постоянным ускорением:")
    print(f"v0 = {calc.get_variable('v0')} м/с")
    print(f"a = {calc.get_variable('a')} м/с²")
    print(f"t = {calc.get_variable('t')} с")

    v = calc.evaluate("v0 + a * t")
    s = calc.evaluate("v0 * t + a * t^2 / 2")
    print(f"Скорость: v = v0 + a*t = {v} м/с")
    print(f"Путь: s = v0*t + a*t²/2 = {s} м")

    # Геометрия
    print("\nГеометрические вычисления:")
    calc.clear_variables()
    calc.set_variable('r', 5)  # радиус
    calc.set_variable('h', 10)  # высота

    circle_area = calc.evaluate("pi * r^2")
    cylinder_volume = calc.evaluate("pi * r^2 * h")
    sphere_volume = calc.evaluate("4/3 * pi * r^3")

    print(f"Радиус: r = {calc.get_variable('r')}")
    print(f"Высота: h = {calc.get_variable('h')}")
    print(f"Площадь круга: {circle_area:.2f}")
    print(f"Объем цилиндра: {cylinder_volume:.2f}")
    print(f"Объем сферы: {sphere_volume:.2f}")

    # Финансовые расчеты
    print("\nФинансовые расчеты:")
    calc.clear_variables()
    calc.set_variable('P', 100000)  # основная сумма
    calc.set_variable('r', 0.05)  # годовая ставка
    calc.set_variable('n', 12)  # количество начислений в год
    calc.set_variable('t', 5)  # количество лет

    # Сложные проценты
    amount = calc.evaluate("P * (1 + r/n)^(n*t)")
    interest = calc.evaluate("P * (1 + r/n)^(n*t) - P")

    print(f"Основная сумма: P = ${calc.get_variable('P'):,.2f}")
    print(f"Годовая ставка: r = {calc.get_variable('r') * 100}%")
    print(f"Период: t = {calc.get_variable('t')} лет")
    print(f"Итоговая сумма: ${amount:,.2f}")
    print(f"Начисленные проценты: ${interest:,.2f}")

    # Пример с вложенными вычислениями
    print("\nВложенные вычисления:")
    calc.clear_variables()

    # Последовательное вычисление с сохранением промежуточных результатов
    calc.set_variable('x', 3)
    calc.set_variable('y', 4)

    # Вычисляем гипотенузу
    calc.set_variable('hyp', calc.evaluate("sqrt(x^2 + y^2)"))

    # Вычисляем углы
    calc.set_variable('alpha', calc.evaluate("atan(y/x) * 180/pi"))
    calc.set_variable('beta', calc.evaluate("90 - alpha"))

    print(f"Катеты: x = {calc.get_variable('x')}, y = {calc.get_variable('y')}")
    print(f"Гипотенуза: {calc.get_variable('hyp'):.2f}")
    print(f"Угол alpha: {calc.get_variable('alpha'):.2f}°")
    print(f"Угол beta: {calc.get_variable('beta'):.2f}°")

    # Проверка
    check = calc.evaluate("sin(alpha*pi/180)^2 + cos(alpha*pi/180)^2")
    print(f"Проверка sin²α + cos²α = {check:.10f}")


def parse_assignment(expression):
    """
    Парсит выражение присваивания вида 'var = expr' или 'var1, var2 = expr1, expr2'.

    Returns:
        list of tuples: [(var_name, expression), ...]
    """
    if '=' not in expression or any(op in expression for op in ['==', '!=', '<=', '>=']):
        return None

    parts = expression.split('=', 1)
    left = parts[0].strip()
    right = parts[1].strip()

    # Простое присваивание
    if ',' not in left:
        return [(left.strip(), right)]

    # Множественное присваивание
    vars = [v.strip() for v in left.split(',')]
    exprs = [e.strip() for e in right.split(',')]

    if len(vars) != len(exprs):
        raise ValueError("Количество переменных не совпадает с количеством выражений")

    return list(zip(vars, exprs))


# Расширенный пример с множественным присваиванием
if __name__ == "__main__":
    print("\n=== Множественное присваивание ===")
    calc = Calculator()

    # Примеры множественного присваивания
    assignments = [
        "x, y = 10, 20",
        "a, b, c = 1, 2, 3",
        "sin30, cos30 = sin(30*pi/180), cos(30*pi/180)"
    ]

    for assignment in assignments:
        parsed = parse_assignment(assignment)
        if parsed:
            for var_name, expr in parsed:
                value = calc.evaluate(expr)
                calc.set_variable(var_name, value)
                print(f"{var_name} = {value}")
        print()

    print("Все переменные:")
    for name, value in calc.list_variables().items():
        print(f"  {name} = {value}")
