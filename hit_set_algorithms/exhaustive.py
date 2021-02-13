"""
Complete pipeline for exhaustive solution to minimum hit set problem

TODO - update current solution as its pretty shit
     - i guess a bunch else but yeah thats the first part
"""
import itertools
import collections


def prime_decomp(val):
    """
    reduces an int into its prime factors, returning the int if it is itself prime
    """
    divisors = list(set([d if val % d == 0 else val for d in range(2, val//2+1)]))
    divisors = [d for d in divisors if all(d % od != 0 for od in divisors if od != d)]
    if val in [2, 3]:
        divisors = divisors + [val]
    return divisors


def prime_list(num_list):
    """
    transforms a list of ints into a list of lists, where each list consists of the
    prime factors of at least one of the input ints. all duplicates are dropped and
    any lists which are a sub list of another list are removed, thus reducing the
    solution space. outputs list of lists still to compute on and list of elelemnts
    that definately belong in the solution
    """
    prime_decomp_lst = [prime_decomp(i) for i in num_list]
    print(prime_decomp_lst)
    sols = [i for i in prime_decomp_lst if len(i) == 1]
    prime_decomp_lst = [i for i in prime_decomp_lst if i not in sols]
    prime_decomp_sets = [set(l) for l in prime_decomp_lst]
    prime_decomp_lst = [l for l,s in zip(prime_decomp_lst, prime_decomp_sets) if not any(s < other for other in prime_decomp_sets)]
    prime_decomp_lst = [list(t) for t in set(map(tuple, prime_decomp_lst))]
    return [prime_decomp_lst, list(set([i for k in sols for i in k]))]


def solution_reduction(list_list, solutions):
    """
    takes as input the two outputs from prime_list. does some reductions on
    the first of these two to minimise computation. outputs list of definite solutions,
    list of lists yet to check and list of elelements that appear only once in the reduced
    solution space
    """
    sols = []
    solos = []
    el_list = list(itertools.chain.from_iterable(list_list))
    counts = collections.Counter(el_list)
    for i in counts.keys():
        if counts[i] == len(list_list):
            sols.append(i)
            for j in range(len(list_list)):
                list_list[j] = [k for k in list_list[j] if k != i]
    del_lst = []
    for i in range(len(list_list)):
        if len(list_list[i]) == 2:
            sub_lst = [j for j in list_list[i] if j not in solutions]
            if len(sub_lst) == 1:
                del_lst.append(list_list[i])
    list_list = [i for i in list_list if i not in del_lst]
    el_list = list(itertools.chain.from_iterable(list_list))
    counts = collections.Counter(el_list)
    for i in counts.keys():
        if counts[i] == 1:
            solos.append(i)
    return [list_list, sols, solos]


def prime_hitting_set(nums):
    """
    NP hard problem :O i've written the code to brute force it but first it cunningly
    reduces the solution space to ensure minimal computations are done. this reduction
    is a semi farce - im sure there are better more pythonic ways to code it (i.e. less verbose)
    and im sure that many of these methods would be faster still, however its pretty
    efficient now and the output seems correct to me so I'll leave it at this for now i think
    """
    lists = prime_list(nums)
    reduced_lists, sols = lists[0], lists[1]
    further_reduced_lists = solution_reduction(reduced_lists, sols)
    remaining = further_reduced_lists[0]
    sols = sols + [i for k in further_reduced_lists[1] for i in k]
    solos = further_reduced_lists[2]
    # this needs improving:
    remaining = [[i for i in j] for j in remaining]
    for i in range(len(remaining)):
        if len(set(remaining[i]).intersection(sols)) > 0:
            remaining[i] = [j for j in remaining[i] if j not in sols and j not in solos]
    remaining = [i for i in remaining if i != [] and len(i) != 1]  # and len(i) != 1
    potential_solutions = [list(k) for k in itertools.product(*remaining)]
    potential_solutions = [list(set(k + sols)) for k in potential_solutions]  # + [sols]
    potential_solutions = sorted(potential_solutions, key=len)
    minimal_length = len(potential_solutions[0])
    solutions = [k for k in potential_solutions if len(k) == minimal_length]
    solutions = [list(t) for t in set(map(tuple, solutions))]
    return solutions
