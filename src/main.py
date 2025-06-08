from rpn_calculator.parser import parse_str_infix, is_infix, parse_str_postfix
from rpn_calculator.calculator import rpn_calculator
from qui import run_gui
import sys


def main():
    """Интерактивный режим для калькулятора"""
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        run_cli()
    else:
        run_gui()


def run_cli():
    """Консольный режим"""
    print("RPN/Infix Calculator. Введите 'exit' для выхода.")
    env = {}
    while True:
        try:
            line = input(">> ").strip()
            if line.lower() == 'exit':
                print("Завершение работы.")
                break
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
                print(f"{var_name} = {result}")
            else:
                print(f"= {result}")

        except (ValueError, TypeError, ZeroDivisionError) as e:
            print(f"Ошибка: {e}")
        except KeyboardInterrupt:
            print("\nЗавершение работы.")
            break


if __name__ == "__main__":
    main()
