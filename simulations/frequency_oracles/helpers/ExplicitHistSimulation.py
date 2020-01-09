import numpy as np

from algorithms.bnst_ldp.Bitstogram.ExplicitHist import ExplicitHist
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from collections import Counter


class ExplicitHistSimulation:
    def __init__(self, params):
        self.epsilon = params["epsilon"]

    def run(self, data, domain):
        # -------------------- Simulating the client-side process --------------------
        ldp_data = []

        print(domain)

        # ExplicitHist privatises strings, so this ensure the index_mapper correctly maps domain values to indexes
            # The ExplicitHist class auto casts data/domain elements to strings so we don't need to do that here
        index_map = lambda x: list(map(str, domain)).index(x) # Index map for indexing hist -> Look at ExplicitHist.py for more info

        hist = ExplicitHist(data, len(domain), self.epsilon, index_map=index_map)
        # -------------------- Simulating the server-side process --------------------
        print("Estimating frequencies...")
        ldp_freq = np.empty(len(domain))
        ldp_plot_data = np.empty(len(domain))

        # Generate both frequency data from the oracle and plot data to be graphed
        for i, item in enumerate(domain):
            ldp_freq[i] = hist.freq_oracle(str(item))  # Freq Oracle
            ldp_plot_data = np.append(ldp_plot_data, [item] * int(round(ldp_freq[i])))  # Generate estimated dataset

        return ldp_plot_data

    def calculate_error(self, data, ldp_plot_data, domain):
        original_freq_data = dict(Counter(data.tolist()))
        ldp_freq_data = dict(Counter(ldp_plot_data.tolist()))

        max_error = 0
        avg_error = 0
        max_bin = 0

        for item in domain:
            error = abs(ldp_freq_data.get(item, 0) - original_freq_data.get(item, 0))
            if max_error < error:
                max_error = error
                max_item = item
            avg_error += error

        avg_error = avg_error / len(domain)

        print("Average Error: " + str(avg_error))
        print("Max Error: " + str(max_error) + " occurs at bin " + str(max_bin))