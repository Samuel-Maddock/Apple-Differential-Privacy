import numpy as np
import pandas as pd

from collections import Counter
from algorithms.bnst_ldp.TreeHistogram.ServerSide import TreeHistogram
from algorithms.apple_ldp.sfp.HeavyHitterList import HeavyHitterList
from simulations.heavy_hitters.helpers.HeavyHitterSimulation import HeavyHitterSimulation


class TreeHistogramSimulation(HeavyHitterSimulation):
    def __init__(self, params):
        super().__init__()
        self.l = params["l"]
        self.w = params["w"]
        self.epsilon = params["epsilon"]
        self.max_string_length = params["max_string_length"]
        self.gram_length = params["gram_length"]
        self.threshold = params["threshold"]
        self.alphabet = params["alphabet"]

    def run(self, data):
        data = pd.DataFrame(list(dict(Counter(data)).items()), columns=["word", "trueFrequency"])

        num_n_grams = int(self.max_string_length / self.gram_length)

        tree_histogram = TreeHistogram(self.l, self.w, self.epsilon, num_n_grams, self.gram_length, self.threshold, self.alphabet)

        word_freq = tree_histogram.runServerSideWordDiscovery(data)

        heavy_hitters = HeavyHitterList(len(word_freq))

        for item in word_freq:
            heavy_hitters.append(item)

        print(data)
        return heavy_hitters.get_data()
