import numpy as np

from algorithms.bnst_ldp.Bitstogram.ExplicitHist import ExplicitHist
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from collections import Counter

from simulations.frequency_oracles.helpers.FrequencyOracleSimulation import FrequencyOracleSimulation


class ExplicitHistSimulation(FrequencyOracleSimulation):
    def __init__(self, params):
        self.epsilon = params["epsilon"]
        self.name = "explicit_hist"

    def run(self, data, domain):
        # -------------------- Simulating the client-side process --------------------
        ldp_data = []

        # ExplicitHist privatises strings, so this ensure the index_mapper correctly maps domain values to indexes
            # The ExplicitHist class auto casts data elements to strings so we don't need to do that here
        index_map = lambda x: list(map(str, domain)).index(str(x)) # Index map for indexing hist -> Look at ExplicitHist.py for more info

        hist = ExplicitHist(data, self.epsilon, len(domain), index_map=index_map)

        # -------------------- Simulating the server-side process --------------------
        ldp_freq = np.empty(len(domain))
        ldp_plot_data = np.empty(len(domain))

        # Generate both frequency data from the oracle and plot data to be graphed
        for i, item in enumerate(domain):
            ldp_freq[i] = hist.freq_oracle(str(item))  # Freq Oracle
            ldp_plot_data = np.append(ldp_plot_data, [item] * int(round(ldp_freq[i])))  # Generate estimated dataset

        return ldp_plot_data