import numpy as np
import math
import itertools
import random
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from collections import Counter

# Any set [n] = {1,...,n} is represented here as {0,....,n-1} for ease of indexing

class Hashtogram:
    def __init__(self, dataset, hash_family, T, epsilon):
        self.epsilon = epsilon
        self.prob = 1 / ((math.e ** epsilon) + 1)
        self.n = len(dataset)
        self.T = T
        self.R = len(hash_family)
        self.hash_family = hash_family
        self.partition = self.__generate_partition(self.n)

        # Constructing randomised dataset (Step 1 of algorithm 7)
        self.y = [0] * self.n
        self.Z = np.random.choice([1, -1], size=(self.T, self.n))
        for j in range(0, self.n):
            r = 0

            for i, partition in enumerate(self.partition):
                if j in partition:
                    r = i

            self.y[j] = self.__basic_randomiser(self.Z[self.hash_family[r](str(dataset[j])), j])

    # Algorithm 4
    def __basic_randomiser(self, x):
        return np.random.choice([x, -x], 1, p=[1 - self.prob, self.prob])[0]

    # Public Randomness Partition - Rework this into a general client-server model
    def __generate_partition(self, n):
        p = np.arange(n)
        np.random.shuffle(p)
        return np.array_split(p, self.R)

    # Step 2 of Algorithm 7, creates an oracle for a specific partition
    def __freq_partition_estimate(self,r,t):
        const = ((math.e ** self.epsilon) + 1) / ((math.e ** self.epsilon) - 1)

        sum = 0
        for j in self.partition[r]:
            sum = sum + (self.y[j] * self.Z[t,j])
        return const * sum

    # Step 2 and 3 of Algorithm 7
    def freq_oracle(self, v):
        freq = 0
        const = ((math.e ** self.epsilon) + 1) / ((math.e ** self.epsilon) - 1)

        frequency_estimates = [0] * self.R

        for i in range(0, self.R):
            hashed_data = self.hash_family[i](str(v))

            frequency_estimates[i] = self.__freq_partition_estimate(i, hashed_data)

        return self.R * np.mean(frequency_estimates)

    def unravel(self):
        return self.y, self.Z, self.partition

