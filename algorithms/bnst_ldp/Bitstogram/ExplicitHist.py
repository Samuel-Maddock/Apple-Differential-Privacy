import numpy as np
from scipy.linalg import hadamard
import math


class ExplicitHist:
    # The ExplicitHist algorithm requires us to set values of our matrix by using the value of the data to be privatised as an index
    # To get around this for non-integer data, we use an index_map, which takes a data element and produces an index of the matrix
        # Typically we use a hash function to do this

    def __init__(self, dataset, epsilon, domain_size, index_map=lambda x: x):
        self.epsilon = epsilon
        self.prob = 1 / ((math.e ** epsilon) + 1)
        self.n = len(dataset)
        self.d = domain_size
        self.index_map = index_map # The index_map -> See SuccintHist.py and ExplicitHistSimulation.py for examples

        if domain_size is None:
            domain = set(dataset)
            self.index_map = lambda x: list(map(str, domain)).index(str(x)) # Index map based on the index of the element in the domain

        # Constructing randomised dataset (Step 1 of algorithm 5)
        self.y = [0] * self.n
        self.Z = np.random.choice([1, -1], size=(self.d, self.n))

        for j in range(0,self.n):
            i = self.index_map(dataset[j])
            self.y[j] = self.__basic_randomiser(self.Z[i, j])

    # Algorithm 4
    def __basic_randomiser(self, x):
        return np.random.choice([x, -x], 1, p=[1 - self.prob, self.prob])[0]

    # Step 2 of Algorithm 5
    def freq_oracle(self, v):
        freq = 0
        for j in range(0, self.n):
            i = self.index_map(v)
            freq += self.y[j] * self.Z[i, j]

        const = ((math.e ** self.epsilon) + 1) / ((math.e ** self.epsilon) - 1)

        return const * freq