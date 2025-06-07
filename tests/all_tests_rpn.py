import unittest
from math import isclose

from main import rpn_calculator, parse_str_postfix, parse_str_infix


class TestPush(unittest.TestCase):

    def test_positive(self):
        program = "42"
        program = parse_str_postfix(program)
        result = rpn_calculator(program)
        self.assertEqual(result, 42, "Could not push positive integer")

    def test_negative(self):
        program = "-13"
        program = parse_str_postfix(program)
        result = rpn_calculator(program)
        self.assertEqual(result, -13, "Could not push negative integer")

    def test_excessive_spaces(self):
        program = "       69       "
        program = parse_str_postfix(program)
        result = rpn_calculator(program)
        self.assertEqual(result, 69, "Could not push integer with excessive spaces")

    def test_extra_on_stack(self):
        program = "42 69"
        program = parse_str_postfix(program)
        self.assertRaises(ValueError, rpn_calculator, program)

    def test_empty(self):
        program = ""
        program = parse_str_postfix(program)
        self.assertRaises(ValueError, rpn_calculator, program)

    def test_nonnum_push(self):
        program = " рофель "
        program = parse_str_postfix(program)
        self.assertRaises(ValueError, rpn_calculator, program)


class TestAddition(unittest.TestCase):

    def test_add_positives(self):
        str_program = "27 42 +"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 69, "Could not add two positive integers")

    def test_add_negatives(self):
        str_program = "-56 -13 +"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, -69, "Could not add two negative integers")

    def test_add_pos_neg(self):
        str_program = "100 -31 +"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 69, "Could not add negative to positive integer")

    def test_add_neg_pos(self):
        str_program = "-42 111 +"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 69, "Could not add positive to negative integer")

    def test_add_excessive_spaces(self):
        str_program = " 228  192     + "
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 420, "Could not add integers with excessive spaces")

    def test_add_not_enough_nums(self):
        str_program = "42 +"
        program = parse_str_postfix(str_program)
        self.assertRaises(ValueError, rpn_calculator, program)

    def test_add_extra_nums(self):
        str_program = "228 69 42 +"
        program = parse_str_postfix(str_program)
        self.assertRaises(ValueError, rpn_calculator, program)


class TestSubtraction(unittest.TestCase):

    def test_sub_positives(self):
        str_program = "69 27 -"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 42, "Could not subtract two positive integers")

    def test_sub_negatives(self):
        str_program = "-111 -69 -"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, -42, "Could not subtract two negative integers")

    def test_sub_pos_neg(self):
        str_program = "56 -13 -"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 69, "Could not subtract negative from positive integer")

    def test_sub_neg_pos(self):
        str_program = "-42 27 -"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, -69, "Could not subtract positive from negative integer")

    def test_sub_excessive_spaces(self):
        str_program = " 420  192     - "
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 228, "Could not subtract integers with excessive spaces")

    def test_sub_not_enough_nums(self):
        str_program = "42 -"
        program = parse_str_postfix(str_program)
        self.assertRaises(ValueError, rpn_calculator, program)

    def test_sub_extra_nums(self):
        str_program = "228 69 42 -"
        program = parse_str_postfix(str_program)
        self.assertRaises(ValueError, rpn_calculator, program)


class TestMultiplication(unittest.TestCase):

    def test_mul_positives(self):
        str_program = "23 3 *"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 69, "Could not multiply two positive integers")

    def test_mul_negatives(self):
        str_program = "-21 -2 *"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 42, "Could not multiply two negative integers")

    def test_mul_pos_neg(self):
        str_program = "57 -4 *"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, -228, "Could not multiply negative and positive integer")

    def test_mul_neg_pos(self):
        str_program = "-42 10 *"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, -420, "Could not multiply positive and negative integer")

    def test_mul_excessive_spaces(self):
        str_program = " 191  7     * "
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 1337, "Could not multiply integers with excessive spaces")

    def test_mul_not_enough_nums(self):
        str_program = "42 *"
        program = parse_str_postfix(str_program)
        self.assertRaises(ValueError, rpn_calculator, program)

    def test_mul_extra_nums(self):
        str_program = "228 69 42 *"
        program = parse_str_postfix(str_program)
        self.assertRaises(ValueError, rpn_calculator, program)


class TestDivision(unittest.TestCase):

    def test_div_positives(self):
        str_program = "207 3 //"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 69, "Could not divide two positive integers")

    def test_div_negatives(self):
        str_program = "-294 -7 //"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 42, "Could not divide two negative integers")

    def test_div_pos_neg(self):
        str_program = "228 -4 //"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, -57, "Could not divide positive by negative integer")

    def test_div_neg_pos(self):
        str_program = "-420 60 //"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, -7, "Could not divide negative by positive integer")

    def test_div_excessive_spaces(self):
        str_program = " 621  9     // "
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 69, "Could not divide integers with excessive spaces")

    def test_div_not_enough_nums(self):
        str_program = "42 //"
        program = parse_str_postfix(str_program)
        self.assertRaises(ValueError, rpn_calculator, program)

    def test_div_extra_nums(self):
        str_program = "228 69 42 //"
        program = parse_str_postfix(str_program)
        self.assertRaises(ValueError, rpn_calculator, program)


class TestPrograms(unittest.TestCase):

    def test_1(self):
        str_program = "7 2 3 * -"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 1, "Program-test №1 didn't pass")

    def test_2(self):
        str_program = "1 2 + 4 * 3 +"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 15, "Program-test №2 didn't pass")

    def test_complex(self):
        str_program = "3 6 3 * 1 4 - 2 ^ // +"
        program = parse_str_postfix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 5, "Program-test complex didn't pass")

    def test_similar(self):
        str_program = "10 15 - 3 *"
        program = parse_str_postfix(str_program)
        result1 = rpn_calculator(program)

        str_program = "3 10 15 - *"
        program = parse_str_postfix(str_program)
        result2 = rpn_calculator(program)

        self.assertEqual(result1, result2, "Results of similar programs are not equal")
        self.assertEqual(result1, -15, "test_similar() calculations are invalid")


class TestInfixPrograms(unittest.TestCase):

    def test_no_space(self):
        str_program = "3+6*(3-2)"
        program = parse_str_infix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, eval(str_program), "InfixProgram-no-space didn't pass")

    def test_with_space(self):
        str_program = "5 * 3 + 2 ^ 4 % 5"
        program = parse_str_infix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 16, "InfixProgram-with-space didn't pass")

    def test_1(self):
        str_program = "6 * (3-5) ^ 2"
        program = parse_str_infix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, 24, "InfixProgram-test №1 didn't pass")

    def test_2(self):
        str_program = "36 // 12"
        program = parse_str_infix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, eval(str_program), "InfixProgram-test №2 didn't pass")

    def test_3(self):
        str_program = "5 * 3 // (6 - 1)"
        program = parse_str_infix(str_program)
        result = rpn_calculator(program)
        self.assertEqual(result, eval(str_program), "InfixProgram-test №3 didn't pass")


class TestUnaryAndFloatOperations(unittest.TestCase):

    def test_unary_neg(self):
        expr = parse_str_postfix("5 neg")
        self.assertEqual(rpn_calculator(expr), -5.0)

    def test_sqrt_positive(self):
        expr = parse_str_postfix("9 sqrt")
        self.assertEqual(rpn_calculator(expr), 3.0)

    def test_sqrt_negative(self):
        expr = parse_str_postfix("-4 sqrt")
        with self.assertRaises(ValueError):
            rpn_calculator(expr)

    def test_sin(self):
        expr = parse_str_postfix("3.14159265 sin")
        result = rpn_calculator(expr)
        self.assertTrue(isclose(result, 0.0, abs_tol=1e-6))

    def test_cos(self):
        expr = parse_str_postfix("0 cos")
        result = rpn_calculator(expr)
        self.assertTrue(isclose(result, 1.0, abs_tol=1e-6))

    def test_tan(self):
        expr = parse_str_postfix("0 tan")
        result = rpn_calculator(expr)
        self.assertTrue(isclose(result, 0.0, abs_tol=1e-6))

    def test_float_operations(self):
        expr = parse_str_postfix("2.5 3.1 +")
        result = rpn_calculator(expr)
        self.assertTrue(isclose(result, 5.6, abs_tol=1e-6))


if __name__ == "__main__":
    unittest.main()
