import numpy as np
import pandas as pd

from collections import Counter
from algorithms.bnst_ldp.TreeHistogram.ServerSide import TreeHistogram
from algorithms.apple_ldp.sfp.HeavyHitterList import HeavyHitterList

import time
import math

class TreeHistogramSimulation():
    def __init__(self, params):
        super().__init__()
        self.l = params["l"]
        self.w = params["w"]
        self.epsilon = params["epsilon"]
        self.max_string_length = params["max_string_length"]
        self.gram_length = params["gram_length"]
        self.threshold = params["threshold"]
        self.alphabet = params["alphabet"]

        self.freq_oracle = params.get("freq_oracle")
        self.freq_oracle_params = params.get("freq_oracle_params")

    def run(self, data):

        # Client-side
        start_time = time.time()

        num_n_grams = int(self.max_string_length / self.gram_length)

        tree_histogram = TreeHistogram(self.l, self.w, self.epsilon, num_n_grams, self.gram_length, self.threshold, self.alphabet)

        client_time = time.time() - start_time
        start_time = time.time()

        # Server-side

        if self.freq_oracle is not None and self.freq_oracle_params is not None:
            word_freq = tree_histogram.run_server_side_word_discovery(data, self.freq_oracle, self.freq_oracle_params)
        else:
            word_freq = tree_histogram.run_server_side_word_discovery(data)

        heavy_hitters = HeavyHitterList(len(word_freq))

        for item in word_freq:
            if item[1] >= math.sqrt(len(data)):
                heavy_hitters.append(item)

        server_time = time.time() - start_time

        return heavy_hitters.get_data(), client_time, server_time
