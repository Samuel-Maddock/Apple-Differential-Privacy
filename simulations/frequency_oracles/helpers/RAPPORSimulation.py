import numpy as np

from algorithms.google_ldp.rappor.server.RAPPORServer import RAPPORServer
from collections import Counter

import time


class RAPPORSimulation():
    def __init__(self, params):
        super().__init__()
        self.num_bloombits = params["num_bloombits"]
        self.num_hashes = params["num_hashes"]
        self.num_of_cohorts = params["num_of_cohorts"]
        self.prob_p = params["prob_p"]
        self.prob_q = params["prob_q"]
        self.prob_f = params["prob_f"]

        self.name = "RAPPOR"

    def run(self, data, domain):
        # -------------------- Simulating the client-side process --------------------
        start_time = time.time()
        rappor_server = RAPPORServer(self.num_bloombits,
                                     self.num_hashes, self.num_of_cohorts,
                                     [self.prob_p, self.prob_q, self.prob_f])

        for i in range(0, len(data)):
            rappor_client = rappor_server.init_client_instance(np.random.randint(0, self.num_of_cohorts - 1))
            rappor_server.add_report(rappor_client.generate_report(str(data[i])))

        client_time = time.time() - start_time

        # -------------------- Simulating the server-side process --------------------
        start_time = time.time()
        hist = rappor_server.generate_freq_hist(list(map(str, domain)))

        ldp_plot_data = np.zeros(len(domain))
        for row in hist.values.tolist():
            ldp_plot_data = np.append(ldp_plot_data, [int(row[0])] * int(row[1]))

        server_time = time.time() - start_time

        return ldp_plot_data, client_time, server_time
