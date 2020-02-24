import numpy as np

from algorithms.bnst_ldp.Bitstogram.ExplicitHist import ExplicitHist
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from collections import Counter, OrderedDict


class FrequencyOracleSimulation:

    def __init__(self):
        self.name = "Frequency Oracle"
        pass

    def run(self, data, domain):
        assert("Must implement")

    def __calculate_error(self, data, ldp_data, domain):
        original_freq_data = dict(Counter(data.tolist()))
        ldp_freq_data = dict(Counter(ldp_data.tolist()))

        max_error = 0
        avg_error = 0
        max_item = ""

        for item in domain:
            error = abs(ldp_freq_data.get(item, 0) - original_freq_data.get(item, 0))
            if max_error < error:
                max_error = error
                max_item = item
            avg_error += error

        avg_error = avg_error / len(domain)

        return max_error, max_item, avg_error

    def generate_stats(self, data, ldp_data, domain):
        row = OrderedDict()
        max_error, max_item, avg_error = self.__calculate_error(data, ldp_data, domain)

        row["freq_oracle"] = self.name
        row["average_error"] = avg_error
        row["max_error"] = max_error
        row["max_item"] = max_item

        return row

