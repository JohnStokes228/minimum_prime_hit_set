"""
functions used throughout the project

"""


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
