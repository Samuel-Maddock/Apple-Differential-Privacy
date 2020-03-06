import numpy as np

from algorithms.apple_ldp.cms.client.ClientCMS import ClientCMS
from algorithms.apple_ldp.cms.server.ServerCMS import ServerCMS
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from collections import Counter
import time


class CMSSimulation():
    def __init__(self, params, is_hcms=False):
        self.k = params["k"]
        self.m = params["m"]
        self.epsilon = params["epsilon"]
        self.is_hcms = is_hcms

        self.name = "cms" if not is_hcms else "hcms"

    def run(self, data, domain):
        # -------------------- Simulating the client-side process --------------------
        hash_funcs = cms_helper.generate_hash_funcs(self.k, self.m)

        ldp_data = []

        start = time.process_time()
        client_cms = ClientCMS(self.epsilon, hash_funcs, self.m)

        for i in range(0, len(data)):
            if self.is_hcms:
                ldp_data.append(client_cms.client_hcms(data[i]))
            else:
                ldp_data.append(client_cms.client_cms(data[i]))

        # -------------------- Simulating the server-side process --------------------

        # Create a sketch matrix of the ldp data
        server_cms = ServerCMS(ldp_data, self.epsilon, self.k, self.m, hash_funcs, is_hadamard=self.is_hcms) # Initialise the frequency oracle
        ldp_plot_data = np.empty(len(domain))

        # Generate both frequency data from the oracle and plot data to be graphed
        for i, item in enumerate(domain):
            ldp_plot_data = np.append(ldp_plot_data, [item] * int(round(server_cms.freq_oracle(item)))) # Generate estimated dataset

        return ldp_plot_data