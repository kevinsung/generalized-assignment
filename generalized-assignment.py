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
    return np.reshape(res.x, (m, n))

def buildGraph(x, p):
    """
    Convert an LP solution to a bipartite graph with fractional
    edge weights where one side represents jobs and the other side
    represents slots
    Inputs:
        x: an mxn matrix
        p: an mxn matrix. These are the job completion times.
        It's required because we need to sort the rows
        of x based on the entries of p.
    Output: a nxmxn array B, where B[j, i, s] represents the weight
    on the edge from job j to slot s of machine i.
    """
    m = x.shape[0]
    n = x.shape[1]

    B = np.zeros((n, m, n))

    for i in range(m):
        s = 0       # current slot in machine i
        left = 1    # space left in current slot
        x_indices = np.argsort(-p[i]) # indices of x when p_i is in nondecreasing order
        for j in x_indices:
            y = x[i, j]
            if y <= left:
                # we can fit this job into slot s
                B[j, i, s] = y
                left -= y
            else:
                # we need to split this job into two slots
                B[j, i, s] = left       # fill up current slot
                s += 1                  # increment slot
                B[j, i, s] = y - left   # put remaining weight in new slot
                left = 1 - (y - left)   # update space left in new slot

    return B

def roundLPSol(x, p):
    """
    Round an LP solution to an integer solution
    Inputs:
        x: an mxn matrix representing a fractional assignment
        p: an mxn matrix. These are the job completion times.
        It's required because we need to sort the rows
        of x based on the entries of p.
    Output: an mxn matrix
    """
    B = buildGraph(x, p)
    return 0

def main():
    p = np.array([[4,4,4],[5,5,5],[5,4,4]])
    c = np.array([[4,4,4],[5,5,5],[5,4,4]])
    T = 50
    x = getLPSol(p, c, T)
    B = buildGraph(x, p)
    print(B)

if __name__ == '__main__':
    main()
