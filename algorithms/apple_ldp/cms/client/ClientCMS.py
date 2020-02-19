import numpy as np
from scipy.linalg import hadamard
import math
import time

class ClientCMS:
    def __init__(self, epsilon, hash_funcs, m):
        self.epsilon = epsilon
        self.hash_funcs = hash_funcs
        self.k = len(hash_funcs)
        self.m = m
        self.prob = 1/(1+math.pow(math.e, self.epsilon/2))

    def __privatise(self, data, is_hadamard=False):
        j = np.random.randint(0, self.k)
        h_j = self.hash_funcs[j]
        v = [0]*self.m if is_hadamard else [-1]*self.m
        v[h_j(data)] = 1
        b = np.random.choice([-1, 1], 1 if is_hadamard else self.m, p=[self.prob, 1-self.prob])
        return v,b,j

    def client_cms(self, data):
        v,b,j = self.__privatise(data)
        return np.multiply(v, b), j

    # Fast-Walsh Hadamard Transform for O(nlogn) performance
        # https://en.wikipedia.org/wiki/Fast_Walsh–Hadamard_transform
    def fwht(self, a):
        """In-place Fast Walsh–Hadamard Transform of array a."""
        h = 1
        while h < len(a):
            for i in range(0, len(a), h * 2):
                for j in range(i, i + h):
                    x = a[j]
                    y = a[j + h]
                    a[j] = x + y
                    a[j + h] = x - y
            h *= 2
        return a

    def client_hcms(self, data):
        if not (self.m & (self.m - 1)) == 0:
            raise ValueError("m must be a positive integer, and m must be a power of 2 to use hcms")

        v,b,j = self.__privatise(data, is_hadamard=True)
        w = self.fwht(v) # Hadamard transform H_m.v

        l = np.random.randint(0, self.m)
        return b[0]*w[l], j, l # Return (b*w_l, index j, index l)
