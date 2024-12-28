# MPCS56430 - Introduction to Scientific Computing
# Assignment 1: Sonia Sharapova
### Written Questions for Part b
### Question 1
#### Considering the numeric types used in this calculation, what is the actual accuracy of this calculation?
Based on the pattern observed, the calculation’s accuracy is dependent on
the number of points in the simulation. The estimate of π gets closer to its true
value with the more points, or darts, thrown. Given the nature of the calculations computed in python, the accuracy is limited by floating-point precision.
#### Question 2
Given your implementation, approximate how long it would take to compute π
to 70,030 digits.
Since the number of points in the Monte Carlo simulation is proportional to
the precision of π, and based on the trends in the benchmarking table, it would
take an extremely large number of points and significant computation time to
reach a precision of 70,030 digits. A different (faster) programming language
like C could be used when the number of points gets exponentially larger, or
the computation method could be revised. The Monte Carlo Method itself may
be a limitation as it might not be the most effective/efficient method. Based on
the Reddit post referenced below, methods such as Gaussian elimination may be more efficient.

### References:
### Links to resources used:
#### 
- Python Accuracy: Overleaf Documentation (https://docs.python.org/3/tutorial/floatingpoint.html)
- Python Speed: Comparisons (https://www.monterail.com/blog/is-python-slow)
- Similar Problems (used as a reference): Monte Carlo Simulation with Python (https://pbpython.com/monte-carlo.html)
- Matplotlib (used as a reference): Documentation (https://matplotlib.org/stable/users/index.html)
- Python Regular Expressions: Documentation (https://docs.python.org/3/library/re.html)
- Reddit Post referenced in Q2: (https://www.reddit.com/r/learnprogramming/comments/10ew6zx/what_are_some_efficient_alternatives_to_a_monte/?rdt=49745)

- Used GenAI for a few some clarifications on how to use yield in Python (for Ex.1 in Part c). It also gave pointers for making the code more efficient using regex.
