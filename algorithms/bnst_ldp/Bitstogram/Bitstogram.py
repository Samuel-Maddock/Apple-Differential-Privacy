import numpy as np
import math
import itertools
import random
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from algorithms.bnst_ldp.Bitstogram.Hashtogram import Hashtogram
from collections import Counter
from reedsolo import RSCodec
from bitstring import BitArray


class Bitstogram:
    def __init__(self, dataset, hash_family, T, binary_domain_size, epsilon):
        self.epsilon = epsilon
        self.prob = 1 / ((math.e ** epsilon) + 1)
        self.n = len(dataset)
        self.T = T
        self.R = len(hash_family)
        self.dataset = dataset
        self.hash_family = hash_family
        self.binary_domain_size = binary_domain_size
        self.partition = self.__generate_partition()
        #self.rs = RSCodec()

        # Constructing randomised dataset
        c = {}
        for j in range(0, self.n):
            c[j] = BitArray(bytes=bytes(dataset[j], "UTF-8")).bin
            #c[j] = BitArray(bytes=self.rs.encode(dataset[j])).bin # Store binary string so we can sample bits
        self.c = c

        S = np.zeros([self.R, self.binary_domain_size]).astype(np.object)

        for r in range(0, self.R):
            for l in range(0, self.binary_domain_size):
                s = []
                for v in self.partition[r][l]:
                    s.append((self.hash_family[r](self.c[v]), str(c[v][l])))
                S[r][l] = s
        self.S = S

    def __basic_randomiser(self, x):
        return np.random.choice([x, -x], 1, p=[1 - self.prob, self.prob])

    # Public Randomness Partition - Rework this into a general client-server model
    def __generate_partition(self):
        p = np.arange(self.n)
        np.random.shuffle(p)
        first_split = np.array_split(p, self.R)
        partition = {}

        for i, split in enumerate(first_split):
            a = np.array_split(split, self.binary_domain_size)
            partition[i] = a

        return partition

    def find_heavy_hitters(self):

        # Generate Hashtograms on all partitions
        histograms = np.zeros([self.R, self.binary_domain_size]).astype(np.object)
        for r in range(0, self.R):
            for l in range(0, self.binary_domain_size):
                histograms[r][l] = Hashtogram(self.S[r, l], self.hash_family, self.T, self.epsilon / 2)

        # Build up heavy-hitters over all partitions
        heavy_hitters = []
        for r in range(0, self.R):
            for t in range(0, self.T):
                # Build up the heavy hitter for a specific partition bit by bit
                v = ""
                for l in range(0, self.binary_domain_size):
                    partition_hist = histograms[r, l]

                    if partition_hist.freq_oracle((t, "0")) >= partition_hist.freq_oracle((t, "1")):
                        v = v + "0"
                    else:
                        v = v + "1"

                try:
                    #heavy_hitters.append(self.rs.decode(BitArray(bin=v).tobytes()))  # Decode the error correcting code
                    heavy_hitters.append(str(BitArray(bin=v).tobytes(), "UTF-8"))
                except:
                    pass

        # Obtain a frequency oracle for the whole dataset
        hist = Hashtogram(self.dataset, self.hash_family, self.T, self.epsilon / 2)

        # Return the heavy-hitters and their estimated frequencies
        return list(map(lambda x: (x, hist.freq_oracle(x)), heavy_hitters))  # Output heavy hitters + freq estimation


# Synthetic data
data1 = ["1011"] * 10000
data2 = ["1111"] * 8000
data3 = ["1000"] * 300

data = np.concatenate((data1,data2,data3))

# We use T = 2, d = 10, epsilon = 1
    # Our threshold is 2, since our original dataset only contains 3 unique elements

T = 10
R = 10
epsilon = 1

h = cms_helper.generate_hash_funcs(R, T)
heavy_hitters = Bitstogram(data, h, T, 32, epsilon)

heavy_hitter_list = heavy_hitters.find_heavy_hitters()

print(heavy_hitter_list)