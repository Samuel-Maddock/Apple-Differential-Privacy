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
    def __init__(self, dataset, hash_family, T, word_length, epsilon):
        self.epsilon = epsilon
        self.prob = 1 / ((math.e ** epsilon) + 1)
        self.n = len(dataset)
        self.T = T
        self.R = len(hash_family)
        self.dataset = dataset
        self.hash_family = hash_family

        ecc_bytes = 2
        self.max_string_length = word_length
        self.binary_domain_size = 8*(self.max_string_length + ecc_bytes)
        self.rs = RSCodec(ecc_bytes)
        self.partition = self.__generate_partition()

        self.padding_char = "*"

        # Constructing randomised dataset
        c = {}
        for j in range(0, self.n):
            data = dataset[j]

            # Pad strings that are smaller than some arbitrary max value
            if len(data) < self.max_string_length:
                data += (self.max_string_length - len(data)) * self.padding_char
            elif len(data) > self.max_string_length:
                data = data[0:self.max_string_length]

            encoded_data = self.rs.encode(data)
            c[j] = BitArray(bytes=encoded_data).bin # Store binary string so we can sample bits
            #c[j] = BitArray(bytes=bytes(dataset[j], "UTF-8")).bin
            if j == 0:
                print(len(c[j]))
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
                histograms[r][l] = Hashtogram(self.S[r, l], self.hash_family, self.T, self.epsilon/2)

        # Build up heavy-hitters over all partitions
        heavy_hitters = set()
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
                    v_bytes = self.rs.decode(BitArray(bin=v).tobytes()) # Decode the error correcting code
                    heavy_hitters.add(v_bytes.decode("utf-8"))
                except:
                    pass

        # Obtain a frequency oracle for the whole dataset
        hist = Hashtogram(self.dataset, self.hash_family, self.T, self.epsilon / 2)
        heavy_hitter_list = []
        print(heavy_hitter_list)
        # Return the heavy-hitters and their estimated frequencies
        for hitter in heavy_hitters:
            freq = hist.freq_oracle(hitter)
            if freq > math.sqrt(self.n):
                heavy_hitter_list.append((hitter, freq))

        return heavy_hitter_list  # Output heavy hitters + freq estimation
