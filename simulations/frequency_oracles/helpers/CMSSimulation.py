import numpy as np

from algorithms.apple_ldp.cms.client.ClientCMS import ClientCMS
from algorithms.apple_ldp.cms.server.SketchGenerator import SketchGenerator
from algorithms.apple_ldp.cms.server.ServerCMS import ServerCMS
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from collections import Counter


class CMSSimulation:
    def __init__(self, params, is_hcms=False):
        self.k = params["k"]
        self.m = params["m"]
        self.epsilon = params["epsilon"]
        self.is_hcms = is_hcms

    def run(self, data, domain):
        # -------------------- Simulating the client-side process --------------------
        hash_funcs = cms_helper.generate_hash_funcs(self.k, self.m)

        ldp_data = []

        client_cms = ClientCMS(self.epsilon, hash_funcs, self.m)
        sketch_generator = SketchGenerator(self.epsilon, self.k, self.m)

        print("Sampling data from the clients...")
        for i in range(0, len(data)):
            if self.is_hcms:
                ldp_data.append(client_cms.client_hcms(data[i]))
            else:
                ldp_data.append(client_cms.client_cms(data[i]))

        # -------------------- Simulating the server-side process --------------------

        # Create a sketch matrix of the ldp data
        if self.is_hcms:
            M = sketch_generator.create_hcms_sketch(ldp_data)
        else:
            M = sketch_generator.create_cms_sketch(ldp_data)

        server_cms = ServerCMS(M, hash_funcs) # Initialise the frequency oracle

        print("Estimating frequencies from sketch matrix...")
        ldp_freq = np.empty(len(domain))
        ldp_plot_data = np.empty(len(domain))

        # Generate both frequency data from the oracle and plot data to be graphed
        for i, item in enumerate(domain):
            ldp_freq[i] = server_cms.estimate_freq(item) # Freq Oracle
            ldp_plot_data = np.append(ldp_plot_data, [item]*int(round(ldp_freq[i]))) # Generate estimated dataset

        return ldp_plot_data

    def calculate_error(self, data, ldp_plot_data, domain):
        original_freq_data = dict(Counter(data.tolist()))
        ldp_freq_data = dict(Counter(ldp_plot_data.tolist()))

        max_error = 0
        avg_error = 0
        max_bin = 0

        for item in domain:
            error = abs(ldp_freq_data.get(item, 0)-original_freq_data.get(item, 0))
            if max_error < error:
                max_error = error
                max_item = item
            avg_error += error

        avg_error = avg_error/len(domain)

        print("Average Error: " + str(avg_error))
        print("Max Error: " + str(max_error) + " occurs at bin " + str(max_bin))