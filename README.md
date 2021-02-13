# minimum_prime_hit_set

In this project I will explore multiple methods of solving the minimum hitting set problem, focusing my efforts 
primarily on using it to find the minimum set of common factors for integers in a list. 

The three current methods I have identified for doing this are:
- exhaustive solution: just solve it even though its NP hard
- greedy solution: solve it greedily, I anticipate this could cause issues since half of all ints are even and 
therefore divisible by 2.
- genetic solution: I'm not fully decided on the details but i think this problem could be a good candidate for a 
stochastic solution of some sort, and GA are interesting to me.
- descent? yeah some kind of gradient descent might also work. could even anneal lol.

so yeah that's the plan so far. We're going to start by building each solution type as an importable pipeline, and then 
look to explore utility and interactions properly in some kind of notebook. all solutions will be thoroughly tested and 
more professionally documented as I've not really done any of that sort of shite in my own work until now. 

I also at some point should write a better explanation as an intro to this project - thus far my readme's have been 
shall we say somewhat lacking to be charitable.