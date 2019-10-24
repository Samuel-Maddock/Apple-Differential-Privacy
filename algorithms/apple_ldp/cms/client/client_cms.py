import numpy as np
import math

def client_cms(epsilon,data,hash_funcs, m):
    j = np.random.randint(0, len(hash_funcs))
    h_j = hash_funcs[j]
    v = [-1]*m
    v[h_j(data)] = 1
    prob = 1/(1+math.pow(math.e, epsilon/2))
    b = np.random.choice([-1, 1], m, p=[prob, 1-prob])
    return np.multiply(v, b), j