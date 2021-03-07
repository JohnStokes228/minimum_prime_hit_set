"""
All algorithm code will be stored here. so far includes exhaustive, stochastic and greedy solutions.

TODO - write GA <what will this look like?>
        - conjure up breeding function / s
        - conjure up mutation function / s
        - conjure up method of generating an initial solution <- this is probs going to be the random code?
     - write any other algorithms
     - consider multiprocessed approach to multiple-stochastic alg.
     - consider method of passing optional params to more complicated algorithms i.e. 'heat' for our descent method,
     or number_of_iterations for the multiple run algorithms
     - consider method of testing stochastic algs, whose output will be to some extent random
"""
import itertools
import collections
import operator
import pandas as pd
import random
from shared_functions import (
    get_sols,
    get_remaining,
    get_prime_decomposition_list,
    check_if_solved,
    solution_reduction,
)


def self_solve_hitting_set(
    remaining,
    sols
):
    """Output the potentially partial solution generated during the self solve phase of the algorithm.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.

    Returns
    -------
    list
        list of integers forming an at least partial solution to MinHitSet.
    """
    print('\n---| Running Self Solving Minimum Prime Hitting Set Algorithm |---\n')
    print('\tSelf Solve has generated the partial solution = {}'.format(sorted(sols)))

    return sols


def randomly_generated_hitting_set(
    remaining,
    sols,
):
    """Run a chaotic mess of a method to solve MinHitSet on remaining decompositions.
    legit though, it just generates a number of random sets and sees which if any is the smallest legitimate solution
    its come up with. If none work, it'll just output a list of every distinct element involved which is a hitset but
    most likely isn't the minimum one.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.

    Returns
    -------
    list
        list of integers forming an at least partial solution to MinHitSet.
    """
    print('\n---| Running Chaotic Random Minimum Prime Hitting Set Algorithm |---\n')

    element_list = list(set(itertools.chain.from_iterable(remaining)))

    potential_sols = [list(set([random.choice(element_list) for i in range(len(element_list))]))
                      for i in range(len(remaining))]
    actual_sols = [sol for sol in potential_sols if not check_if_solved(remaining, sol)]

    if len(actual_sols) > 0:
        best_sol = min(actual_sols, key=len) + sols
    else:
        best_sol = element_list + sols

    print('\tMinHitSet complete! solution = {}'.format(sorted(best_sol)))

    return best_sol


def exhaustive_hitting_set(
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
    print('\n---| Running Exhaustive Minimum Prime Hitting Set Algorithm |---\n')

    partial_hitting_sets = [list(k) for k in itertools.product(*remaining)]
    hitting_sets = [list(set(k + sols)) for k in partial_hitting_sets]
    hitting_sets = sorted(hitting_sets, key=len)

    min_hit_set = hitting_sets[0]
    print('\tMinHitSet complete! solution = {}'.format(sorted(min_hit_set)))

    return min_hit_set


def greedy_hitting_set(
    remaining,
    sols,
):
    """Run Greedy MinHitSet heuristic on remaining un hit solutions.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.

    Returns
    -------
    list
        List of integers forming a potential (greedy) solution to the MinHitSet algorithm run on remaining.
    """
    print('\n---| Running Greedy Minimum Prime Hitting Set Heuristic |---\n')

    unsolved = True
    while unsolved:
        element_list = list(itertools.chain.from_iterable(remaining))
        counts = collections.Counter(element_list)

        next_element_in_sol = max(counts.items(), key=operator.itemgetter(1))[0]
        sols.append(next_element_in_sol)

        remaining = check_if_solved(remaining, sols)
        if not remaining:
            unsolved = False

    print('\tMinHitSet complete! solution = {}'.format(sorted(sols)))

    return sols


def stochastic_descent_hitting_set(
    remaining,
    sols,
):
    """Run stochastic descent MinHitSet algorithm on remaining un hit solutions. The nature of this as a probabilistic
    method means that it will in all likelihood generate different solutions every time.

    TODO - consider allowing worsening steps with some decreasing probability to increase the coverage of the alg?

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.

    Returns
    -------
    list
        List of integers forming a stochastically generated solution to the MinHitSet algorithm run on remaining.
    """
    print('\n---| Running Stochastic Descent Minimum Prime Hitting Set Algorithm |---\n')

    element_list = list(itertools.chain.from_iterable(remaining))
    current_sol = list(set(element_list))
    current_cost = len(current_sol)
    cont = True
    rep = 0

    while cont:
        counts = pd.DataFrame.from_dict(collections.Counter(element_list), orient='index').reset_index()
        counts.columns = ['prime', 'count']

        pick = int(counts['prime'].sample(weights=counts['count']))
        test_sol = [i for i in current_sol if i != pick]

        brakes_hit_set = check_if_solved(remaining, test_sol)
        if not brakes_hit_set:
            current_sol = test_sol
            element_list = [i for i in element_list if i != pick]
            rep = 0
        else:
            rep += 1

        if (current_cost == (len(sols) + 1)) | (rep == 5):
            cont = False

    final_sol = current_sol + sols

    print('\tMinHitSet complete! solution = {}'.format(sorted(final_sol)))

    return final_sol


def multiple_stochastic_descent_hitting_set(
    remaining,
    sols,
):
    """Run multiple stochastic descent MinHitSet algorithms on remaining decompositions and take the best value

    TODO - let number_of_iterations be an input
         - consider a multiprocessed approach

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.

    Returns
    -------
    list
        List of integers forming the best stochastically generated solution to the MinHitSet algorithm run on remaining
        from n runs.
    """
    print('\n---| Running Multiple Stochastic Descent Minimum Prime Hitting Set Algorithm |---\n')

    number_of_iterations = 5
    sols_list = []

    for i in range(number_of_iterations):

        element_list = list(itertools.chain.from_iterable(remaining))
        current_sol = list(set(element_list))
        current_cost = len(current_sol)
        cont = True
        rep = 0

        while cont:
            counts = pd.DataFrame.from_dict(collections.Counter(element_list), orient='index').reset_index()
            counts.columns = ['prime', 'count']

            pick = int(counts['prime'].sample(weights=counts['count']))
            test_sol = [i for i in current_sol if i != pick]

            brakes_hit_set = check_if_solved(remaining, test_sol)
            if not brakes_hit_set:
                current_sol = test_sol
                element_list = [i for i in element_list if i != pick]
                rep = 0
            else:
                rep += 1

            if (current_cost == (len(sols) + 1)) | (rep == 5):
                cont = False

        final_sol = current_sol + sols
        sols_list.append(final_sol)

    best_sol = min(sols_list, key=len)
    print('\tMinHitSet complete! best solution = {}'.format(sorted(best_sol)))

    return best_sol


def genetic_hitting_set(
    remaining,
    sols,
):
    """Run GA MinHitSet on remaining un hit solutions.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.

    Returns
    -------
    list
        List of integers forming a genetically generated solution to the MinHitSet algorithm run on remaining.
    """
    print('\n---| Running Genetic Minimum Prime Hitting Set Algorithm |---\n')

    initial_population = []

    # find parent candidates <- look for best sols, prehaps still somewhat randomly sample?

    # generate children <- need some method of breeding that will generate legit sols

    # mutate some random sample <- need some method of mutation that will generate legit sols

    # decide whether enough is enough? <- will we set number of iterations first or have some criteria?

    print('\tMinHitSet complete! solution = {}'.format(sorted(sols)))

    return sols


def get_chosen_algorithm(algorithm):
    """Function to return function to run algorithm on.

    Parameters
    ----------
    algorithm : string
        Name of algorithm to return.

    Returns
    -------
    function
        Uncalled function of desire
    """
    algorithms_dict = {
        'self-solve': self_solve_hitting_set,
        'random': randomly_generated_hitting_set,
        'exhaustive': exhaustive_hitting_set,
        'greedy': greedy_hitting_set,
        'stochastic': stochastic_descent_hitting_set,
        'multiple-stochastic': multiple_stochastic_descent_hitting_set,
        'genetic': genetic_hitting_set,
    }

    try:
        desired_function = algorithms_dict[algorithm]
        return desired_function
    except KeyError:
        print('{} is not an available algorithm'.format(algorithm))
        return None


def minimum_prime_hitting_set(
        int_list,
        algorithm='exhaustive',
):
    """Run MinPrimeHitSet algorithm.

    Parameters
    ----------
    int_list : list
        List of integers to run the algorithm on.
    algorithm : string
        Pick algorithm to be utilised in solution, takes values of 'exhaustive', 'greedy', 'stochastic'.

    Returns
    -------
    list / None
        List of integers that form *a* solution to MinPrimeHitSet for some input list of integers. Multiple solutions
        may exist and since no seed is set I think it is possible that this could output different lists each time if
        multiple solutions do exist. Returns None if no valid algorithm is selected
    """
    prime_decomposition_list = get_prime_decomposition_list(int_list)

    sols = get_sols(prime_decomposition_list)

    remaining = get_remaining(prime_decomposition_list, sols)
    remaining = check_if_solved(remaining, sols)
    remaining = solution_reduction(remaining, sols)

    if (type(remaining[0]) != list) and (algorithm != 'self-solve'):
        return remaining
    else:
        try:
            sols = get_chosen_algorithm(algorithm)(remaining, sols)
            return sols
        except TypeError:
            print('partial solution = {}'.format(sols))
            return sols
