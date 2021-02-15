"""
Unit tests for the functions that are shared across multiple algorithms.

"""
from shared_functions import prime_factor_decomposition
import unittest


class TestSharedFunctions(unittest.TestCase):

    def test_prime_factor_decomposition(self):
        input_ints = [10, 2, 5, -12, 36, 100, 0]
        expected_output = [[2, 5], [2], [5], [2, 3], [2, 3], [2, 5], []]
        realised_output = []

        for input_int in input_ints:
            realised_output.append(prime_factor_decomposition(input_int))

        self.assertListEqual(expected_output, realised_output)


if __name__ == '__main__':
    unittest.main(exit=True)
