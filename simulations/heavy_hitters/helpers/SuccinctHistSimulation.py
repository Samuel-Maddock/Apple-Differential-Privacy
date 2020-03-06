from collections import Counter

from algorithms.bnst_ldp.Bitstogram.SuccinctHist import SuccintHist
from algorithms.apple_ldp.sfp.HeavyHitterList import HeavyHitterList

class SuccinctHistSimulation():
    def __init__(self, params):
        super().__init__()
        self.epsilon = params["epsilon"]
        self.T = params["T"]
        self.max_string_length = params["max_string_length"]
        self.d = self.max_string_length * 8

    def run(self, data):

        succinct_hist = SuccintHist(data, self.T, self.d, self.epsilon, self.max_string_length)

        word_estimates = succinct_hist.find_heavy_hitters()

        heavy_hitters = HeavyHitterList(len(word_estimates))

        for item in word_estimates:
            heavy_hitters.append(item)

        return heavy_hitters.get_data()
