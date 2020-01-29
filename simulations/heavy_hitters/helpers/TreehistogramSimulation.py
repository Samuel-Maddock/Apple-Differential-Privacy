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
        self.num_n_grams = params["num_n_grams"]
        self.gram_length = params["gram_length"]
        self.threshold = params["threshold"]

    def run(self, data):

        data = pd.DataFrame(list(dict(Counter(data)).items()), columns=["word", "trueFrequency"])

        tree_histogram = TreeHistogram(self.l, self.w, self.epsilon, self.num_n_grams, self.gram_length, self.threshold)

        word_freq = tree_histogram.runServerSideWordDiscovery(data)

        heavy_hitters = HeavyHitterList(len(word_freq))

        for item in word_freq:
            heavy_hitters.append(item)

        print(data)
        return heavy_hitters.get_data()
