"""
functions used by multiple methods

TODO - probably rename the file lets be real 'shared_functions' is hardly clear
"""
import itertools
import collections
import random


def prime_factor_decomposition(val):
    """Reduce any integer into its unique prime decomposition, returning the input integer if the integer itself is
    prime.

    Parameters
    ----------
    val : int
        An integer to be decomposed

    Returns
    -------
    list
        List of prime factors of val, or an empty list if val is in [-1, 0, 1]
    """
    val = abs(val)

    if val not in [0, 1]:
        divisors = list(set([d if val % d == 0 else val
                             for d in range(2, val // 2 + 1)]))
        divisors = [d for d in divisors
                    if all(d % od != 0 for od in divisors if od != d)]

        if val in [2, 3]:
            divisors = divisors + [val]

        return divisors

    else:
        return []


def get_prime_decomposition_list(int_list):
    """Break a list of integers down into their unique prime factors

    Parameters
    ----------
    int_list : list
        List of integers to factorise.

    Returns
    -------
    list
        List of prime factor decompositions for input list.
    """
    print('\ndecomposing input integers...\n')
    prime_decomposition_list = [prime_factor_decomposition(i) for i in int_list
                                if prime_factor_decomposition(i) != []]

    return prime_decomposition_list


def get_sols(prime_decomposition_list):
    """Get list of ints that are definitely within the solution to MinHItSet alg.

    Parameters
    ----------
    prime_decomposition_list : list
        List of lists of prime numbers

    Returns
    -------
    list
        List of unique integers that were previously elements of all sub lists in prime_decomposition_list of length 1.
    """
    sols = [decomposition for decomposition in prime_decomposition_list
            if len(decomposition) == 1]
    sols = list(set(itertools.chain(*sols)))

    return sols


def get_remaining(
    prime_decomposition_list,
    sols,
):
    """Get list of all sub lists that are not included in the solution directly.

    steps included:
    1. get all decompositions not included in sols.
    2. remove all remaining decompositions that are subsets of other decompositions i.e. [2, 3], [3, 2, 7] -> [3, 2, 7]

    Parameters
    ----------
    prime_decomposition_list : list
        List of lists of prime numbers
    sols : list
        List of integers which if present as a list in prime_decomposition_list should be dropped.

    Returns
    -------
    list
        List of lists where each sublist if of length > 1.
    """
    sols = [[i] for i in sols]

    remaining = [decomposition for decomposition in prime_decomposition_list
                 if decomposition not in sols]
    remaining_sets = [set(decomposition) for decomposition in remaining]

    remaining = [decomposition_list for decomposition_list, decomposition_set in zip(remaining, remaining_sets)
                 if not any(decomposition_set < other for other in remaining_sets)]

    return remaining


def check_if_solved(
    remaining,
    sols,
):
    """Check if sols is enough to solve MinHitSet alg.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.

    Returns
    -------
    list
        List of remaining solutions not hit by sols.
    """
    check = []

    for decomposition in remaining:
        check.append(any(item in decomposition for item in sols))

    if all(check):
        return []

    else:
        indices = [i for i, x in enumerate(check) if x is False]
        remaining = [remaining[i] for i in indices]

        return remaining


def check_for_single_remaining_sol(
    remaining,
    sols,
):
    """Check if a single additional int is enough to hit the remaining decompositions.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.

    Returns
    -------
    list
        List of integers representing an at least partial solution to MinHitSet. Adds a random element from the
        available sols in the case where multiple single integers will complete the solution.
    """
    element_list = list(itertools.chain.from_iterable(remaining))
    counts = collections.Counter(element_list)
    check = []

    for key, value in counts.items():
        if value == len(remaining):
            check.append(key)

    if len(check) > 0:
        sols.append(random.choice(check))

    return sols


def remove_single_elements(remaining):
    """Remove elements that appear only once in the solution, if they appear in a decomposition containing at least one
    other element that appears more than once.

    Parameters
    ---------
    remaining : list
        List of lists of prime numbers.

    Returns
    -------
    list
        List of lists of remaining prime factor decompositions, with single elements removed from each sublist.
    """
    element_list = list(itertools.chain.from_iterable(remaining))
    counts = collections.Counter(element_list)

    solo_elements = [key for key, value in counts.items()
                     if value == 1]

    for decomposition in range(len(remaining)):
        if (
                any(element in solo_elements for element in remaining[decomposition])
                and (not all(element in solo_elements for element in remaining[decomposition]))
        ):
            remaining[decomposition] = [i for i in remaining[decomposition]
                                        if i not in solo_elements]

    return remaining


def solution_reduction(
    remaining,
    sols,
):
    """Run the solution space reduction steps on remaining.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.

    Returns
    -------
    list
        List of either lists or ints depending on whether the reduction is enough to solve the algorithm or not.
    """
    print('checking if problem solved without need for chosen algorithm...\n')

    if len(remaining) == 0:
        print('\tMinHitSet complete! solution = {}'.format(sols))
        return sols
    else:
        sols = check_for_single_remaining_sol(remaining, sols)
        remaining = check_if_solved(remaining, sols)

        if len(remaining) == 0:
            print('\tMinHitSet complete! solution = {}'.format(sols))
            return sols
        else:
            remaining = remove_single_elements(remaining)
            return remaining
