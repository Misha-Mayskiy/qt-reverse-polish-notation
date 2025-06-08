import re


def is_infix(expr: str) -> bool:
    """Проверяет, является ли выражение инфиксным, ища операторы или скобки."""
    return bool(re.search(r'[+\-*/^%()]', expr))


def parse_str_postfix(s: str) -> str:
    """Чистка строки от лишних пробелов."""
    return " ".join(s.strip().split())


def parse_str_infix(ex: str) -> str:
    """Преобразование инфиксного выражения в обратную польскую нотацию."""
    OPERATORS = {
        '+': (1, 'L'), '-': (1, 'L'),
        '*': (2, 'L'), '//': (2, 'L'), '%': (2, 'L'),
        '^': (3, 'R'), 'neg': (4, 'R')
    }
    FUNCTIONS = {"sin", "cos", "tan", "sqrt", "abs"}

    def tokenize(expression):
        token_regex = re.compile(r'(\d+\.\d*|\d*\.\d+|\d+)|([a-zA-Z_][a-zA-Z0-9_]*)|(//|%|[+\-*/^()])')
        tokens = []
        for num, name, op in token_regex.findall(expression):
            if num:
                tokens.append(num)
            elif name:
                tokens.append(name)
            elif op:
                tokens.append(op)
        return tokens

    output = []
    stack = []
    tokens = tokenize(ex)
    prev_token_type = 'OPERATOR'

    for token in tokens:

        if (re.fullmatch(r'\d+\.\d*|\d*\.\d+|\d+', token)
                or token not in OPERATORS and token not in FUNCTIONS and token not in '()'):
            output.append(token)
            prev_token_type = 'OPERAND'

        elif token in FUNCTIONS:
            stack.append(token)
            prev_token_type = 'FUNCTION'
        elif token == '-':

            if prev_token_type in ('OPERAND', 'PAREN_CLOSE'):
                op = '-'
            else:
                op = 'neg'

            while (stack and stack[-1] in OPERATORS and
                   ((OPERATORS[op][1] == 'L' and OPERATORS[op][0] <= OPERATORS[stack[-1]][0]) or
                    (OPERATORS[op][1] == 'R' and OPERATORS[op][0] < OPERATORS[stack[-1]][0]))):
                output.append(stack.pop())
            stack.append(op)
            prev_token_type = 'OPERATOR'

        elif token in OPERATORS:
            while (stack and stack[-1] in OPERATORS and
                   ((OPERATORS[token][1] == 'L' and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]) or
                    (OPERATORS[token][1] == 'R' and OPERATORS[token][0] < OPERATORS[stack[-1]][0]))):
                output.append(stack.pop())
            stack.append(token)
            prev_token_type = 'OPERATOR'

        elif token == '(':
            stack.append(token)
            prev_token_type = 'PAREN_OPEN'

        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack or stack[-1] != '(':
                raise ValueError("Несбалансированные скобки или пропущен открывающий символ")
            stack.pop()
            if stack and stack[-1] in FUNCTIONS:
                output.append(stack.pop())
            prev_token_type = 'PAREN_CLOSE'

    while stack:
        op = stack.pop()
        if op in ['(', ')']:
            raise ValueError("Несбалансированные скобки в выражении")
        output.append(op)

    return ' '.join(output)
