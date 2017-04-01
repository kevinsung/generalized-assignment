import numpy as np
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
    return 0

def buildGraph(x):
    """
    Convert an LP solution to a bipartite graph where one side
    represents jobs and the other side represents slots
    Inputs:
        x: an mxn matrix
    Output: a 3-d array B. B[j,i,s] represents weight on edge
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
