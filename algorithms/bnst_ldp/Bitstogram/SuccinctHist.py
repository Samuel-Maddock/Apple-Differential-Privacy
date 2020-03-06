import numpy as np
import math
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from algorithms.bnst_ldp.Bitstogram.Hashtogram import Hashtogram
from algorithms.bnst_ldp.Bitstogram.ExplicitHist import ExplicitHist
from bitstring import BitArray

# Any set [n] = {1,...,n} is represented here as {0,....,n-1} for ease of indexing
# d is the binary length of the strings in the dataset

class SuccintHist:
    def __init__(self, dataset, T, d, epsilon, max_string_length):
        self.epsilon = epsilon
        self.prob = 1 / ((math.e ** epsilon) + 1)
        self.n = len(dataset)
        self.T = T
        self.hash = cms_helper.generate_hash(T, 2)
        self.binary_domain_size = d
        self.partition = self.__generate_partition(self.n)
        self.dataset = dataset
        self.padding_char = "*"
        self.max_string_length = max_string_length

        # Constructing randomised dataset
        S = {}
        for l in range(0, self.binary_domain_size):
            tuple_set = []
            for v in self.partition[l]:
                data = dataset[v]

                # Pad strings that are smaller than the max length string in the dataset
                if len(data) < self.max_string_length:
                    data += (self.max_string_length - len(data)) * self.padding_char
                elif len(data) > self.max_string_length:
                    data = data[0:self.max_string_length]

                tuple_set.append((self.hash(data), BitArray(bytes=bytes(data, "utf-8")).bin[l])) # Hash data item and sample lth bit
            S[l] = tuple_set

        self.S = S

    # Public Randomness Partition - Rework this into a general client-server model
    def __generate_partition(self, n):
        p = np.arange(n)
        np.random.shuffle(p)
        return np.array_split(p, self.binary_domain_size)

    def __index_mapper(self, tup):
        # For our threshold T we create an ExplicitHist of length 2T and depending on the coordinate we
            # store the randomised value in either (k, "0") which corresponds to the key k
            # or (k, "1") which is indexed by k + T

        if tup[1] == "0":
            return tup[0]
        else:
            return tup[0]+self.T

    def find_heavy_hitters(self):
        hist_list = []
        for l in range(0, self.binary_domain_size):
            s = self.S[l]
            hist_list.append(ExplicitHist(s, self.epsilon / 2, self.T * 2, index_map=self.__index_mapper))

        S = set()

        for t in range(0, self.T):
            # Build up heavy hitters bit by bit
            v = ""
            for l in range(0, self.binary_domain_size):
                partition_hist = hist_list[l]

                if partition_hist.freq_oracle((t,"0")) >= partition_hist.freq_oracle((t,"1")):
                    v = v + "0"
                else:
                    v = v + "1"

            try:
                S.add(BitArray(bin=v).tobytes().decode("utf-8"))
            except:
                pass # Sometimes random noise will generate strings that can't be decoded to utf-8


        # Below is computationally poor, since we construct a histogram with a matrix of n x n
            # In order to map binary strings to our matrix Z we hash them using a hash that maps our dataset 1-1
            # Again this is computationally poor (in both time and space)
        # The full Bitstogram algorithm deals with this problem
        hist = ExplicitHist(self.dataset, self.epsilon / 2, len(self.dataset),
                            index_map=cms_helper.generate_hash(len(self.dataset), seed=3))

        heavy_hitters = []
        print(S)
        for heavy_hitter in S:
            freq = hist.freq_oracle(heavy_hitter)
            if freq > 3*math.sqrt(len(self.dataset)): # Heuristic to prune false positives
                heavy_hitters.append((heavy_hitter, freq))

        print(heavy_hitters)
        return heavy_hitters # Output heavy hitters + freq estimation