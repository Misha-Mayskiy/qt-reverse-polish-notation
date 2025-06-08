import unittest
from math import isclose, pi, sqrt

from main import rpn_calculator, parse_str_postfix, parse_str_infix, evaluate_program


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

    def test_not_num_push(self):
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


class TestRPNWithVariables(unittest.TestCase):

    def test_addition_with_vars(self):
        expr = "x y +"
        vars = {"x": 5, "y": 7}
        self.assertEqual(rpn_calculator(expr, vars), 12)

    def test_complex_expression(self):
        expr = "a b + c * d neg +"
        vars = {"a": 2, "b": 3, "c": 4, "d": 6}
        self.assertEqual(rpn_calculator(expr, vars), 14)

    def test_float_and_int_mix(self):
        expr = "a b *"
        vars = {"a": 2.5, "b": 4}
        self.assertAlmostEqual(rpn_calculator(expr, vars), 10.0)

    def test_missing_variable(self):
        expr = "x y +"
        vars = {"x": 1}
        with self.assertRaises(ValueError):
            rpn_calculator(expr, vars)

    def test_with_unary_functions(self):
        expr = "x sqrt"
        vars = {"x": 9}
        self.assertEqual(rpn_calculator(expr, vars), 3.0)

    def test_with_trigonometric(self):
        expr = "x sin"
        vars = {"x": 0}
        self.assertEqual(rpn_calculator(expr, vars), 0.0)

    def test_infix_with_vars(self):
        infix = "a + b * 2 + neg a"
        rpn = parse_str_infix(infix)
        result = rpn_calculator(rpn, {"a": 3, "b": 4})
        self.assertEqual(result, 8)


class TestRPNAssignment(unittest.TestCase):

    def test_single_assignment(self):
        lines = ["x = 2 3 +"]
        result = evaluate_program(lines)
        self.assertEqual(result["x"], 5)

    def test_multiple_assignments(self):
        lines = [
            "a = 4",
            "b = 5",
            "c = a b +"
        ]
        result = evaluate_program(lines)
        self.assertEqual(result, {"a": 4, "b": 5, "c": 9})

    def test_infix_assignment(self):
        lines = ["x = 3 + 4 * 2"]
        result = evaluate_program(lines)
        self.assertEqual(result["x"], 11)

    def test_combination_postfix_and_infix(self):
        lines = [
            "x = 3",
            "y = x 2 +",
            "z = y * 2 + 1"
        ]
        result = evaluate_program(lines)
        self.assertEqual(result["z"], 11)

    def test_just_expression(self):
        lines = [
            "a = 4",
            "b = 2",
            "a b +"
        ]
        result = evaluate_program(lines)
        self.assertEqual(result["a"], 4)
        self.assertEqual(result["b"], 2)

    def test_invalid_variable_name(self):
        lines = ["1a = 5"]
        with self.assertRaises(ValueError):
            evaluate_program(lines)

    def test_empty_and_whitespace_lines(self):
        lines = [
            "    ",
            "x = 2 2 +",
            "   ",
            "y = x 2 *"
        ]
        result = evaluate_program(lines)
        self.assertEqual(result["x"], 4)
        self.assertEqual(result["y"], 8)


class TestRPNVectorOperations(unittest.TestCase):

    def test_vector_addition(self):
        self.assertEqual(rpn_calculator("[1,2,3] [4,5,6] +"), [5, 7, 9])

    def test_vector_subtraction(self):
        self.assertEqual(rpn_calculator("[5,5,5] [2,1,0] -"), [3, 4, 5])

    def test_scalar_multiplication(self):
        self.assertEqual(rpn_calculator("[2,4] 3 *"), [6, 12])
        self.assertEqual(rpn_calculator("3 [2,4] *"), [6, 12])

    def test_vector_negation(self):
        self.assertEqual(rpn_calculator("[1,-2,3] neg"), [-1, 2, -3])

    def test_vector_abs(self):
        result = rpn_calculator("[3,4] abs")
        self.assertTrue(isclose(result, 5.0))

    def test_angle_between_vectors(self):
        result = rpn_calculator("[1,0] [0,1] angle")
        self.assertTrue(isclose(result, pi / 2, abs_tol=1e-6))

    def test_mixed_vector_scalar_operations(self):
        with self.assertRaises(TypeError):
            rpn_calculator("[1,2] 2 +")
        with self.assertRaises(TypeError):
            rpn_calculator("2 [1,2] +")
        with self.assertRaises(TypeError):
            rpn_calculator("[1,2] 3 -")
        with self.assertRaises(TypeError):
            rpn_calculator("3 [1,2] -")

    def test_invalid_vector_length_for_add(self):
        with self.assertRaises(ValueError):
            rpn_calculator("[1,2] [1,2,3] +")

    def test_vector_variable(self):
        result = rpn_calculator("a neg", {"a": [1, 2, -1]})
        self.assertEqual(result, [-1, -2, 1])


class TestRPNMixedTypes(unittest.TestCase):

    def test_scalar_then_vector_operations(self):
        self.assertEqual(rpn_calculator("[1,2] neg"), [-1, -2])

    def test_nested_stack_behavior(self):
        with self.assertRaises(TypeError):
            rpn_calculator("1 2 [1,2] +")

    def test_vector_then_scalar_sequence(self):
        result = rpn_calculator("[1,2,2] abs 3 +")
        self.assertTrue(isclose(result, 6.0))

    def test_angle_with_vectors_and_scalar_ops(self):
        angle = rpn_calculator("[1,0] [0,1] angle 1 +")  # pi/2 + 1
        self.assertTrue(isclose(angle, pi / 2 + 1, abs_tol=1e-6))

    def test_combined_operations(self):
        expr = "2 3 + [1,1] * abs"
        result = rpn_calculator(expr)
        self.assertTrue(isclose(result, sqrt(50), abs_tol=1e-6))

    def test_chained_neg_abs(self):
        result = rpn_calculator("[3,4] neg abs")
        self.assertEqual(result, 5.0)

    def test_vector_angle_with_self(self):
        self.assertTrue(isclose(rpn_calculator("[1,2] [1,2] angle"), 0.0, abs_tol=1e-6))


if __name__ == "__main__":
    unittest.main()
