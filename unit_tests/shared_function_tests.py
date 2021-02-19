"""
Unit tests for the functions that are shared across multiple algorithms.

"""
from shared_functions import (
    prime_factor_decomposition,
    get_sols,
    get_remaining,
    check_if_solved,
    check_for_single_remaining_sol,
    remove_single_elements,
)
import unittest


class TestSharedFunctions(unittest.TestCase):

    def test_prime_factor_decomposition(self):
        input_ints = [10, 2, 5, -12, 36, 100, 0]
        expected_output = [[2, 5], [2], [5], [2, 3], [2, 3], [2, 5], []]
        realised_output = []

        for input_int in input_ints:
            realised_output.append(prime_factor_decomposition(input_int))

        self.assertListEqual(expected_output, realised_output)

    def test_get_sols(self):
        input_list = [[2, 3, 5], [3], [9], [11, 23], [3]]
        expected_output = [3, 9]

        realised_output = get_sols(input_list)

        self.assertCountEqual(expected_output, realised_output)

    def test_get_remaining(self):
        input_list = [[2, 3, 5], [3], [9], [11, 23], [3], [11, 23, 17], [2, 13], [13, 23]]
        input_sols = [3, 9, 2]
        expected_output = [[2, 3, 5], [11, 23, 17], [2, 13], [13, 23]]

        realised_output = get_remaining(input_list, input_sols)

        self.assertCountEqual(expected_output, realised_output)

    def test_check_if_solved_solved(self):
        input_list = [[2, 3, 5], [3], [9], [3], [2, 13]]
        input_sols = [3, 9, 2]
        expected_output = []

        realised_output = check_if_solved(input_list, input_sols)

        self.assertCountEqual(expected_output, realised_output)

    def test_check_if_solved_not_solved(self):
        input_list = [[2, 3, 5], [3], [9], [3], [11, 23, 17], [2, 13], [13, 23]]
        input_sols = [3, 9]
        expected_output = [[11, 23, 17], [2, 13], [13, 23]]

        realised_output = check_if_solved(input_list, input_sols)

        self.assertCountEqual(expected_output, realised_output)

    def test_check_for_single_remaining_sol_true(self):
        input_list = [[5]]
        input_sols = [2, 3]
        expected_output = [2, 3, 5]

        realised_output = check_for_single_remaining_sol(input_list, input_sols)

        self.assertCountEqual(expected_output, realised_output)

    def test_check_for_single_remaining_sol_false(self):
        input_list = [[5, 13], [13], [23, 29]]
        input_sols = [2, 3]
        expected_output = [2, 3]

        realised_output = check_for_single_remaining_sol(input_list, input_sols)

        self.assertCountEqual(expected_output, realised_output)

    def test_remove_single_elements(self):
        input_list = [[2, 3, 13], [27, 2, 3], [27, 5], [11]]
        expected_output = [[2, 3], [27, 2, 3], [27], [11]]

        realised_output = remove_single_elements(input_list)

        self.assertCountEqual(expected_output, realised_output)


if __name__ == '__main__':
    unittest.main(exit=True)
