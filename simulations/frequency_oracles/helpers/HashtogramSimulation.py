import numpy as np

from algorithms.bnst_ldp.Bitstogram.Hashtogram import Hashtogram
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from collections import Counter


class HashtogramSimulation():
    def __init__(self, params, use_median=False):
        super().__init__()
        self.T = params["T"]
        self.R = params["R"]
        self.epsilon = params["epsilon"]
        self.use_median = use_median
        self.name = "hashtogram"

    def run(self, data, domain):
        # -------------------- Simulating the client-side process --------------------
        ldp_data = []
        hash_funcs = cms_helper.generate_hash_funcs(self.R, self.T)

        hashtogram = Hashtogram(data, hash_funcs, self.T, self.epsilon, use_median=self.use_median)

        # -------------------- Simulating the server-side process --------------------
        ldp_freq = np.empty(len(domain))
        ldp_plot_data = np.empty(len(domain))

        # Generate both frequency data from the oracle and plot data to be graphed
        for i, item in enumerate(domain):
            ldp_freq[i] = hashtogram.freq_oracle(str(item))  # Freq Oracle
            ldp_plot_data = np.append(ldp_plot_data, [item] * int(round(ldp_freq[i])))  # Generate estimated dataset

        return ldp_plot_data