import numpy as np

from algorithms.google_ldp.rappor.server.RAPPORServer import RAPPORServer
from collections import Counter


class RAPPORSimulation:
    def __init__(self, params):
        self.num_bloombits = params["num_bloombits"]
        self.num_hashes = params["num_hashes"]
        self.num_of_cohorts = params["num_of_cohorts"]
        self.prob_p = params["prob_p"]
        self.prob_q = params["prob_q"]
        self.prob_f = params["prob_f"]

    def run(self, data, domain):
        # -------------------- Simulating the client and server-side process --------------------

        rappor_server = RAPPORServer(self.num_bloombits,
                                     self.num_hashes, self.num_of_cohorts,
                                     [self.prob_p, self.prob_q, self.prob_f])

        for i in range(0, len(data)):
            rappor_client = rappor_server.init_client_instance(np.random.randint(0, self.num_of_cohorts - 1))
            rappor_server.add_report(rappor_client.generate_report(str(data[i])))

        hist = rappor_server.generate_freq_hist(list(map(str, domain)))

        print(hist)

        ldp_plot_data = np.zeros(len(domain))
        for row in hist.values.tolist():
            ldp_plot_data = np.append(ldp_plot_data, [int(row[0])] * int(row[1]))

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
