"""
All algorithm code will be stored here. so far includes exhaustive, stochastic and greedy solutions.

TODO - write any other algorithms
     - consider multiprocessed approach to multiple-stochastic alg.
     - *consider method of passing optional params to more complicated algorithms i.e. 'heat' for our descent method,
     or number_of_iterations for the multiple run algorithms*
     - consider method of testing stochastic algs, whose output will be to some extent random
"""
import itertools
import collections
import operator
import pandas as pd
import random
from math import floor
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
    text,
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
    text : bool
        Set False to avoid printing any statements

    Returns
    -------
    list
        list of integers forming an at least partial solution to MinHitSet.
    """
    if text:
        print('\n---| Running Chaotic Random Minimum Prime Hitting Set Algorithm |---\n')

    element_list = list(set(itertools.chain.from_iterable(remaining)))

    potential_sols = [list(set([random.choice(element_list) for i in range(len(element_list))]))
                      for i in range(len(remaining))]
    actual_sols = [sol for sol in potential_sols if not check_if_solved(remaining, sol)]

    if len(actual_sols) > 0:
        best_sol = min(actual_sols, key=len) + sols
    else:
        best_sol = element_list + sols

    if text:
        print('\tMinHitSet complete! solution = {}'.format(sorted(best_sol)))

    return best_sol


def exhaustive_hitting_set(
    remaining,
    sols,
    text,
):
    """Run exhaustive MinHitSet algorithm on remaining decompositions.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.
    text : bool
        Set False to avoid printing any statements

    Returns
    -------
    list
        List of integers forming a solution to the MinHitSet algorithm run on remaining.
    """
    if text:
        print('\n---| Running Exhaustive Minimum Prime Hitting Set Algorithm |---\n')

    partial_hitting_sets = [list(k) for k in itertools.product(*remaining)]
    hitting_sets = [list(set(k + sols)) for k in partial_hitting_sets]
    hitting_sets = sorted(hitting_sets, key=len)

    min_hit_set = hitting_sets[0]

    if text:
        print('\tMinHitSet complete! solution = {}'.format(sorted(min_hit_set)))

    return min_hit_set


def greedy_hitting_set(
    remaining,
    sols,
    text,
):
    """Run Greedy MinHitSet heuristic on remaining un hit solutions.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.
    text : bool
        Set False to avoid printing any statements

    Returns
    -------
    list
        List of integers forming a potential (greedy) solution to the MinHitSet algorithm run on remaining.
    """
    if text:
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

    if text:
        print('\tMinHitSet complete! solution = {}'.format(sorted(sols)))

    return sols


def stochastic_descent_hitting_set(
    remaining,
    sols,
    text,
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
    text : bool
        Set False to avoid printing any statements

    Returns
    -------
    list
        List of integers forming a stochastically generated solution to the MinHitSet algorithm run on remaining.
    """
    if text:
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

    if text:
        print('\tMinHitSet complete! solution = {}'.format(sorted(final_sol)))

    return final_sol


def multiple_stochastic_descent_hitting_set(
    remaining,
    sols,
    text,
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
    text : bool
        Set False to avoid printing any statements

    Returns
    -------
    list
        List of integers forming the best stochastically generated solution to the MinHitSet algorithm run on remaining
        from n runs.
    """
    if text:
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

    if text:
        print('\tMinHitSet complete! best solution = {}'.format(sorted(best_sol)))

    return best_sol


def generate_initial_population(
    remaining,
    attempted_population_size=50,
):
    """Generates an initial population of solution to MinHitSet to feed the GA.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    attempted_population_size : int
        Number of attempts at generating a legitimate solution.

    Returns
    -------
    list
        list of solutions to MinHitSet.
    """
    element_list = list(set(itertools.chain.from_iterable(remaining)))

    initial_population = [list(set([random.choice(element_list) for i in range(len(element_list))]))
                          for i in range(attempted_population_size)]
    initial_population = [sol for sol in initial_population if not check_if_solved(remaining, sol)]

    if initial_population:
        initial_population = sorted(initial_population, key=len)
    else:
        initial_population = [element_list]

    return [sol for sol in initial_population if not check_if_solved(remaining, sol)]


def get_parents(
    initial_population,
    number_of_breeding_pairs=10,
):
    """Pick parents from initial population, using weighted sampling with replacement.

    Parameters
    ----------
    initial_population : list
        List of solutions to MinHitSet problem.
    number_of_breeding_pairs : int
        Number of pairs of parents desired

    Returns
    -------
    list
        List of parents chosen.
    """
    initial_population_size = len(initial_population)

    weight_widths = int(initial_population_size / 3)
    weights = [1, 2, 3] * (weight_widths + 1)
    weights = weights[:len(initial_population)]

    parents = random.choices(sorted(initial_population, key=len), weights=weights, k=(2*number_of_breeding_pairs))
    parents = [parents[:number_of_breeding_pairs], parents[number_of_breeding_pairs:]]

    return parents


def breed_sols(parents):
    """Breeding function to generate new solutions out of presumably decent ones

    Parameters
    ----------
    parents : list
        List of two equally long lists, which will be the 'mother' and 'father' of the breeding alg.

    Returns
    -------
    list
        List of children that may or may not be solutions to MinHitSet.
    """
    children = []

    for i in range(len(parents[0])):
        left_sample_size = random.sample(range(1, len(parents[0][i])), k=1)
        right_sample_size = random.sample(range(1, len(parents[1][i])), k=1)

        child = random.sample(parents[0][i], k=left_sample_size[0]) + random.sample(parents[1][i], k=right_sample_size[0])
        children.append(list(set(child)))

    return [child for child in children if child]


def mutate_sols(mutation_candidates):
    """Apply mutation function to the selected candidates.

    Parameters
    ----------
    mutation_candidates : list
        List of lists where each sublist is a potential solution of MinHitSet that will be mutated.

    Returns
    -------
    list
        List of lists where each sublist is a mutated form of one of the input sublists.
    """
    mutants = []

    for candidate in mutation_candidates:
        mutants.append(random.sample(candidate, k=(len(candidate)-1)))

    return [mutant for mutant in mutation_candidates if mutant]


def genetic_hitting_set(
    remaining,
    sols,
    text,
):
    """Run GA MinHitSet on remaining un hit solutions.

    Parameters
    ----------
    remaining : list
        List of lists of remaining decompositions to check if sols hit.
    sols : list
        List of integers that form an at least partial solution to MinHitSet algorithm.
    text : bool
        Set False to avoid printing any statements

    Returns
    -------
    list
        List of integers forming a genetically generated solution to the MinHitSet algorithm run on remaining.
    """
    if text:
        print('\n---| Running Genetic Minimum Prime Hitting Set Algorithm |---\n')

    initial_population = generate_initial_population(remaining)

    best_sol = min(initial_population, key=len)  # current best, to be iterated on
    changed = 0

    while changed < 3:
        parents = get_parents(initial_population)
        children = breed_sols(parents)
        try:
            mutants = mutate_sols(random.choices(initial_population + children, k=20))
        except IndexError:
            mutants = []
        finally:
            initial_population = initial_population + children + mutants
            initial_population = [sol for sol in initial_population if not check_if_solved(remaining, sol) and sol]
            initial_population = sorted(initial_population, key=len)
            initial_population = initial_population[floor(len(initial_population)/10):]

            new_best_sol = min(initial_population, key=len)

            if len(new_best_sol) >= len(best_sol):
                changed += 1
            else:
                changed = 0
                best_sol = new_best_sol

    sols = sols + best_sol

    if text:
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
    text=True,
):
    """Run MinPrimeHitSet algorithm.

    Parameters
    ----------
    int_list : list
        List of integers to run the algorithm on.
    algorithm : string
        Pick algorithm to be utilised in solution, takes values of 'exhaustive', 'greedy', 'stochastic'.
    text : bool
        Set False to avoid printing any statements throughout.

    Returns
    -------
    list / None
        List of integers that form *a* solution to MinPrimeHitSet for some input list of integers. Multiple solutions
        may exist and since no seed is set I think it is possible that this could output different lists each time if
        multiple solutions do exist. Returns None if no valid algorithm is selected
    """
    prime_decomposition_list = get_prime_decomposition_list(int_list, text)

    sols = get_sols(prime_decomposition_list)

    remaining = get_remaining(prime_decomposition_list, sols)
    remaining = check_if_solved(remaining, sols)
    remaining = solution_reduction(remaining, sols, text)

    if (type(remaining[0]) != list) and (algorithm != 'self-solve'):
        return remaining
    else:
        try:
            sols = get_chosen_algorithm(algorithm)(remaining, sols, text)
            return sols
        except TypeError:
            print('partial solution = {}'.format(sols))
            return sols
