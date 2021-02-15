"""
Unit tests for exhaustive algorithm. See function docstrings for explanation of inputs / expected outputs. Some test
cases (most notably hitting_set's) are quite low effort, this is in part due to complexity of manually calculating the
MinHitSet solution, and in part due to the codes current decision to pick to return only one solution in cases where
there are multiple, which is not infrequent for larger input lists. I use assertCountEqual over assertListEqual in most
cases as order is arbitrary and irrelevant.

"""
from hit_set_algorithms.exhaustive import (
    get_sols,
    get_remaining,
    check_if_solved,
    check_for_single_remaining_sol,
    remove_single_elements,
    hitting_set,
    minimum_hitting_set_exhaustive,
)
import unittest


class TestExhaustiveAlgorithmFunctions(unittest.TestCase):

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

    def test_hitting_set(self):
        input_list = [[2, 3, 13], [27, 2, 3], [11], [2, 5]]
        input_sols = [11]
        expected_output = [11, 2]

        realised_output = hitting_set(input_list, input_sols)

        self.assertCountEqual(expected_output, realised_output)

    def test_minimum_hitting_set_exhaustive(self):
        input_list = [2, 3, 5, 10, 25, 15, 9, 4, 38]
        expected_output = [2, 3, 5]

        realised_output = minimum_hitting_set_exhaustive(input_list)

        self.assertCountEqual(expected_output, realised_output)


if __name__ == '__main__':
    unittest.main(exit=True)
