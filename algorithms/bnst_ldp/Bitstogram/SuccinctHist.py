import numpy as np
import math
import itertools
import random
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from algorithms.bnst_ldp.Bitstogram.ExplicitHist import ExplicitHist
from collections import Counter

# Any set [n] = {1,...,n} is represented here as {0,....,n-1} for ease of indexing

# Dataset passed to it should be binary strings of length no more than logd

class SuccintHist:
    def __init__(self, dataset, hash, T, d, epsilon):
        self.epsilon = epsilon
        self.prob = 1 / ((math.e ** epsilon) + 1)
        self.n = len(dataset)
        self.d = d
        self.T = T
        self.hash = hash
        self.binary_domain_size = math.ceil(math.log(d, 2))
        self.partition = self.__generate_partition(self.n)
        self.dataset = dataset

        dataset = [str(i) for i in dataset]

        # Constructing randomised dataset
        S = {}
        for l in range(0, self.binary_domain_size):
            tuple_set = []
            for v in self.partition[l]:
                data = dataset[v]
                tuple_set.append((self.hash(data), data[l])) # Hash data item and sample lth bit
            S[l] = tuple_set

        self.S = S

    def __basic_randomiser(self, x):
        return np.random.choice([x, -x], 1, p=[1 - self.prob, self.prob])

    # Public Randomness Partition - Rework this into a general client-server model
    def __generate_partition(self, n):
        p = np.arange(n)
        np.random.shuffle(p)
        return np.array_split(p, self.binary_domain_size)

    def __index_mapper(self, tup):
        if tup[1] == "0":
            return tup[0]
        else:
            return tup[0]+self.T

    def find_heavy_hitters(self):
        hist_list = []
        for l in range(0, self.binary_domain_size):
            s = self.S[l]
            hist_list.append(ExplicitHist(s, self.T * 2, self.epsilon/2, index_map=self.__index_mapper))

        S = []

        for t in range(0, self.T):
            # Build up heavy hitters bit by bit
            v = ""
            for l in range(0, self.binary_domain_size):
                partition_hist = hist_list[l]

                if partition_hist.freq_oracle((t,"0")) >= partition_hist.freq_oracle((t,"1")):
                    v = v + "0"
                else:
                    v = v + "1"
            S.append(v)


        # Below is computationally poor, since we construct a histogram with a matrix of n x n
            # In order to map binary strings to our matrix Z we hash them using a hash that maps our dataset 1-1
            # Again this is computationally poor (in both time and space)
        # The full Bitstogram algorithm deals with this problem
        hist = ExplicitHist(self.dataset, len(self.dataset), self.epsilon/2, index_map=cms_helper.generate_hash(len(self.dataset), seed=3))

        return list(map(lambda x: (x, hist.freq_oracle(x)), S)) # Output heavy hitters + freq estimation



# Synthetic data
data1 = ["1011"] * 10000
data2 = ["1111"] * 8000
data3 = ["1000"] * 300

data = np.concatenate((data1,data2,data3))

# We use T = 2, d = 10, epsilon = 1
    # Our threshold is 2, since our original dataset only contains 3 unique elements

h = cms_helper.generate_hash(2, 2)
heavy_hitters = SuccintHist(data, h, 2, 10, 1)

heavy_hitter_list = heavy_hitters.find_heavy_hitters()

print(heavy_hitter_list)