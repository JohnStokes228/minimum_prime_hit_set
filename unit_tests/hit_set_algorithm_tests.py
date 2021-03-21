"""
Unit tests for exhaustive algorithm. See function docstrings for explanation of inputs / expected outputs. Some test
cases (most notably hitting_set's) are quite low effort, this is in part due to complexity of manually calculating the
MinHitSet solution, and in part due to the codes current decision to pick to return only one solution in cases where
there are multiple, which is not infrequent for larger input lists. I use assertCountEqual over assertListEqual in most
cases as order is arbitrary and irrelevant.

TODO - GA unit tests - legit this one needs testing fo sho
"""
from hit_set_algorithms import (
    exhaustive_hitting_set,
    greedy_hitting_set,
    minimum_prime_hitting_set,
)
import unittest


class TestExhaustiveAlgorithmFunctions(unittest.TestCase):

    def test_exhaustive_hitting_set(self):
        input_list = [[2, 3, 13], [27, 2, 3], [11], [2, 5]]
        input_sols = [11]
        expected_output = [11, 2]

        realised_output = exhaustive_hitting_set(input_list, input_sols)

        self.assertCountEqual(expected_output, realised_output)

    def test_greedy_hitting_set(self):
        input_list = [[3, 7, 5], [3], [11, 5], [3, 11], [11, 7]]
        input_sols = [2]
        expected_output = [2, 3, 11]

        realised_output = greedy_hitting_set(input_list, input_sols)

        self.assertCountEqual(expected_output, realised_output)

    def test_minimum_prime_hitting_set_exhaustive(self):
        input_list = [2, 3, 5, 10, 25, 15, 9, 4, 38]
        expected_output = [2, 3, 5]

        realised_output = minimum_prime_hitting_set(input_list, algorithm='exhaustive')

        self.assertCountEqual(expected_output, realised_output)

    def test_minimum_prime_hitting_set_greedy(self):
        input_list = [2, 3, 5, 10, 25, 15, 9, 4, 38]
        expected_output = [2, 3, 5]

        realised_output = minimum_prime_hitting_set(input_list, algorithm='greedy')

        self.assertCountEqual(expected_output, realised_output)


if __name__ == '__main__':
    unittest.main(exit=True)
