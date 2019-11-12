import numpy as np
from scipy.linalg import hadamard
import math

class ClientCMS:
    def __init__(self, epsilon, hash_funcs, m):
        self.epsilon = epsilon
        self.hash_funcs = hash_funcs
        self.k = len(hash_funcs)
        self.m = m

        if (self.m & (self.m - 1)) == 0:
            self.hadamard_matrix = hadamard(self.m) # Cache hadamard for performance

    def __privatise(self, data, is_hadamard=False):
        j = np.random.randint(0, self.k)
        h_j = self.hash_funcs[j]
        v = [0]*self.m if is_hadamard else [-1]*self.m
        v[h_j(data)] = 1
        prob = 1/(1+math.pow(math.e, self.epsilon/2))
        b = np.random.choice([-1, 1], 1 if is_hadamard else self.m, p=[prob, 1-prob])
        return v,b,j

    def client_cms(self, data):
        v,b,j = self.__privatise(data)
        return np.multiply(v, b), j

    def client_hcms(self, data):
        if not (self.m & (self.m - 1)) == 0:
            raise ValueError("m must be an positive integer, and m must b a power of 2 to use hcms")

        v,b,j = self.__privatise(data, is_hadamard=True)
        w = self.hadamard_matrix.dot(v) # Hadamard transform H_m.v
        l = np.random.randint(0, self.m)
        return b[0]*w[l], j, l # Return (b*w_l, index j, index l)
