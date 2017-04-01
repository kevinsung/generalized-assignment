import numpy as np
from scipy.optimize import linprog
from matplotlib import pyplot as plt

def getLPSol(p, c, T):
    """
    Get a solution to the LP. There are n jobs and m machines
    Inputs:
        p: an mxn matrix
        c: an mxn matrix
        T: a number
    Output: an mxn matrix
    """
    # get LP dimensions
    m = p.shape[0]
    n = p.shape[1]

    d = np.empty(m * n)         # coefficient vector
    A_ub = np.zeros((m, m * n)) # upper bound constraint matrix
    b_ub = T * np.ones(m)       # upper bound constraint vector
    A_eq = np.zeros((n, m * n)) # equality constraint matrix
    b_eq = np.ones(n)           # equality constraint vector
    bounds = []                 # bounds on variables

    # construct coefficient vector and set variable bounds
    for i in range(m):
        for j in range(n):
            # construct coefficient vector
            d[i * n + j] = c[i, j]
            # set variable bounds
            if p[i, j] > T:
                bounds.append((0, 0))
            else:
                bounds.append((0, None))

    # construct upper bound matrix
    for i in range(m):
        for j in range(n):
            A_ub[i, i * n + j] = p[i, j]

    # construct equality constraint matrix
    for j in range(n):
        for i in range(m):
            A_eq[j, i * n + j] = 1

    # get LP solution
    res = linprog(d, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    return res

def buildGraph(x):
    """
    Convert an LP solution to a bipartite graph where one side
    represents jobs and the other side represents slots
    Inputs:
        x: an mxn matrix
    Output: a 3-d array B. B[j, i, s] represents weight on edge
    from job j to slot s of machine i.
    """
    return 0

def roundLPSol(x):
    """
    Round an LP solution to an integer solution
    Inputs:
        x: an mxn matrix representing a fractional assignment
    Output: an mxn matrix
    """
    B = buildGraph(x)
    return 0

def main():
    p = np.array([[4,4,4],[5,5,5],[5,4,4]])
    c = np.array([[4,4,4],[5,5,5],[5,4,4]])
    T = 50
    res = getLPSol(p, c, T)
    print(res)

if __name__ == '__main__':
    main()
