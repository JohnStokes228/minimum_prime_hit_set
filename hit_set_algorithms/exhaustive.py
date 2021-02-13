"""
Complete pipeline for exhaustive solution to minimum hit set problem

TODO - potentially add a feature to get all solutions rather than just a solution? it probably wouldn't be much extra
       work
"""
import itertools
import collections
import random
from shared_functions import prime_factor_decomposition


def get_sols(prime_decomposition_list):
    """Get list of ints that are definitely within the solution to MinHItSet alg.

    Parameters
    ----------
    prime_decomposition_list : list
        List of lists of prime numbers

    Returns
    -------
    list
        List of unique integers that were previously elements of all sublists in prime_decomposition_list of length 1.
    """
    sols = [decomposition for decomposition in prime_decomposition_list
            if len(decomposition) == 1]
    sols = list(set(itertools.chain(*sols)))

    return sols


def get_remaining(
        prime_decomposition_list,
        sols,
):
    """Get list of all sublists that are yet to be hit by MinHitSet algorithm.

    steps included:
    1. get all decompositions not covered by sols.
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
        indices = [i for i, x in enumerate(check) if x == False]
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
    if len(remaining) == 0:
        print('MinHitSet complete! solution = {}'.format(sols))
        return sols
    else:
        sols = check_for_single_remaining_sol(remaining, sols)
        remaining = check_if_solved(remaining, sols)

        if len(remaining) == 0:
            print('MinHitSet complete! solution = {}'.format(sols))
            return sols
        else:
            remaining = remove_single_elements(remaining)
            return remaining


def hitting_set(
        remaining,
        sols,
):
    """Run exhaustive MinHitSet algorithm on remaining decompositions.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.

    Returns
    -------
    list
        List of integers forming a solution to the MinHitSet algorithm run on remaining.
    """
    partial_hitting_sets = [list(k) for k in itertools.product(*remaining)]
    hitting_sets = [list(set(k + sols)) for k in partial_hitting_sets]
    hitting_sets = sorted(hitting_sets, key=len)

    min_hit_set = hitting_sets[0]

    return min_hit_set


def minimum_hitting_set_exhaustive(num_list):
    """Run exhaustive MinPrimeHitSet algorithm.

    Parameters
    ----------
    num_list : list
        List of integers to run the algorithm on

    Returns
    -------
    list
        List of integers that form *a* solution to MinPrimeHitSet for some input list of integers. Multiple solutions
        may exist and since no seed is set I think it is possible that this could output different lists each time if
        multiple solutions do exist.
    """
    print('\n---| Running Minimum Hitting Set Algorithm |---')

    prime_decomposition_list = [prime_factor_decomposition(i) for i in num_list
                                if prime_factor_decomposition(i) != []]

    sols = get_sols(prime_decomposition_list)

    remaining = get_remaining(prime_decomposition_list, sols)
    remaining = check_if_solved(remaining, sols)

    sol_reduction = solution_reduction(remaining, sols)

    if type(sol_reduction[0]) != list:
        sols = sol_reduction
        return sols
    else:
        remaining = sol_reduction
        sols = hitting_set(remaining, sols)
        print('MinHitSet complete! solution = {}'.format(sols))
        return sols
