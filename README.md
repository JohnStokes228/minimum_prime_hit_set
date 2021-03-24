# Intro to the Minimum Prime Hitting Set Problem

The initial problem to be investigated in this project can be formualted as such:

*For some input list of integers, find the shortest possible list of integers such that each element in the input list is divisible by at least one element in your new list.*

The Minimum Prime Hitting Set (***MinPrimeHitSet***) is a suggested solution to this problem, which in a general sense can be achieved using the following two steps:

- reduce each input integer into a set of its unqiue prime factors
- find the minimum hitting set for the resultant set of sets

This will work due to the set theory lemma that each integer has a unique prime decomposition, and the fact that prime decompositions can be seen as something of an *elementary* form for numbers (i.e. primes are the most basic building blocks of the integers). As such any list that solves the initial problem formulation will be at least as long as the smallest list of primes that solves this problem, and so the initially broad problem has been reduced to one with a much narrower scope. Unfortunately, this problem (MinHitSet) has been proven NP-hard. For this reason there is scope to investigate a multitude of different methods that can provide varying degrees of 'good enough' solutions, to determine which methods can be seen as the most optimal ones to employ in which circumstances.

The project contains a number of .py files, containing the python code to implement the algorithms as described below, all of which are ultimately called from a single function (minimum_prime_hitting_set, in hit_set_algorithms.py) using a string parameter to dictate which method is used. *Most* of the code has been properly unit tested (using unittest rather than pytest sorry :O), however I remain unsure on how to build tests for algorithms with built in randomness so there are certainly some parts of the more complicated algorithms which can be considered 'untested'. Finally, also included is an ipython notebook, which will contain the results of the experiments run using the code in the python files.


# Algorithms Utilised

In this section I'll briefly explain each of the algorithms used in the project. The first of these (self-solve) is a bit funky compared to the rest so do be sure you read that one first even if it seems crap. 

## Self-Solve Partial Algorithm (SfSP)

The Self-Solve algorithm is the only not generalisable algorithm. It's less of an algorithm of its own and more of a set of checks to be preformed that allow someone to potentially instantly solve the general MinHitSet problem, and so will actually form the first step of all the other algorithms. A brief description of the steps involved is:

***Using all active decompositions in the solution space***:
- check for any decompositions of length 1. in order to hit these, the element they contain **must** be contained in the solution
- check if the partial solution formed so far solves the MinHitSet, if so, **END**
- remove all decompositions from the solution space who have been hit by the partial solution.
- check if there exists a single element which hits all remaining decompositions, if so append it to the partial solution, **END**
- else, output the partial solution for further reduction, **END**

Due to the potentially partial nature of the output to this algorithm it will be known from now on as ***SfSP***. It will not be used for comparisons as theres no reason not to run it prior to running any of the other algorithms, and its output will not be an actual solution to the problem in any of the test cases for obvious reasons.

## Random Algorithm (Rand)

The Random algorithm simple generates a list of random permutations of primes present in the decomposition. if any of these end up being actual HitSets then the shortest of them is output as the solution. if None are, then a list of all unique primes present in the decomposition is output instead. 

## Exhaustive Algorithm (Xstv)

The first meaningful algorithm used to solve the problem is the Exhaustive algorithm (hereon refered to as ***Xstv***). When triggered (As you might expect with such a name), the algorithm exhaustively searches for a minimum solution in the remaining active solution space. As such this algorithm is garunteed to output the correct solution, provided you have enough available RAM to calculate all possibilities, and are willing to wait for this to be done. On small enough solution spaces (though not necessarily small data as we'll see) there's no reason not to use this method to solve the problem. A brief description of the steps involved (after running *SfSP*) is:

***Using all active decompositions in the solution space***:
- generate every possible outcome of picking one element from each decomposition
- *for each outcome:*
    - convert the outcome list into a set
    - measure its length
- take the shortest length outcome and append it to any results from *SfSP*

**END**

## Greedy Heuristic (Grdy)

The greedy heuristic (***Grdy***) was the first algorithm that could potentially output a suboptimal yet complete solution. My thoughts prior to testing the algorithms preformance is that I expect to see a signifcant decrease in run time compared to *Xstv* for more complicated problems, but at the cost of a slight (?) hit in accuracy. In particular, due to the fact that half of all integers are even, I expect this heuristic in most circumstances to output a list containing the number 2, which may not truly belong in the solution. I'd be interested to see what effect this has on the length of the output solution (does it just output a solution of length = min + 1? or does the inclusion of the 2 completely change the solution it comes too?) A brief description of the steps involved (after running *SfSP*) is:

***Using all active decompositions in the solution space***:
- get occurance counts for each unique element across all active decompositions
- append the most frequently occuring element to *SfSP*
- check if MinHitSet is solved, if so **END**
- if not, remove all decompositions that are now hit by the new partial solution, repeat from first step.


## Stochastic Descent Algorithm (Dcnt)

The first of several stochastic methods, Descent (***Dcnt***) is designed to work backwards from the longest possible solution until some criteria is hit. Its about the most basic form of descent immaginable, and doesnt attempt anything even mildly funky like annealing as I'm not convinced these would be helpful in this use case. In particular, note that it never takes a step that would worsen its standing - this is quite uncommon and I think unrecommended in the field of stochastic descent methods, this might be something we change eventualy. A brief description of the steps involved (after running *SfSP*) is:

***Using all active decompositions in the solution space***:
<br>i = 0 
<br>N = *some predetermined value, defaults to 5 I think*
- create a list of all unique elements across all active decompositions. This will form the maximum hit set for the solution space.
- using inverse frequency of occurance to provide weights, randomly pick an element to remove from the current solution. 
- While i < N
    - if current solution is a hitting set:
        - i = 0
        - break
        else:
        - i += 1
        - repeat from step 2

**END**

This algorithm is the one I expect to have the worst accuracy, and to be honest I cant see it running in less time that *Grdy* either. Basically anticipate dissapointement and you cant be let down ;). My expectation however is that due to the randomness involved, it will provide a decent way of generating several possible solutions and checking for the best, which *could* have better final preformance than the *Grdy*, leading us too...:

## Best Stochastic Descent Algorithm (Dcn+)

The next stochastic method is a simple expansion on the first, in which you run multiple *Dcnt* algorithms and simply take the best output to be the solution. This algoirthm will be known as ***Dcn+*** as it takes the bestest output from *Dcnt*. I actually wouldnt be supprised to see this one end up being one of the more accurate of the bunch, but its run time is not going to be fast depending on how many *Dcnt*'s are run. I guess with proper vectorisation and multiprocessing implementation though anything is possible...?

## Genetic Algorithm (GenA)

An unnecessary algorithm i coded up just for the fun of it. The steps post self solve are as follows:

<br>j = 0
- generate i initial solutions at random
- using solution length as weights, pick 2n solutions with replacement to serve as parents
- take a random number of elements from each parent and combine them to form a child
- pick m random solutions and remove an element from each at random, to mutate it
- check the length of the shortest current solution. 
    - if shorter than the previous shortest, continue
    - else j += 1
- if j = 3:
<br>**END**
    
