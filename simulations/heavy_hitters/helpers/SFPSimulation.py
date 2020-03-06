import numpy as np

from algorithms.apple_ldp.sfp.server.ServerSFP import ServerSFP
from algorithms.apple_ldp.sfp.client.ClientSFP import ClientSFP
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from algorithms.apple_ldp.sfp.HeavyHitterList import HeavyHitterList


import math
from collections import Counter


class SFPSimulation():
    def __init__(self, params):
        super().__init__()
        self.epsilon = params["epsilon"]
        self.m = params["m"]
        self.k = params["k"]
        self.epsilon_prime = params["epsilon_prime"]
        self.m_prime = params["m_prime"]
        self.k_prime = params["k_prime"]
        self.threshold = params["threshold"]
        self.alphabet = params["alphabet"]

        self.fragment_length = params.get("fragment_length")
        self.max_string_length = params.get("max_string_length")

        if params.get("freq_oracle") is not None or params.get("freq_oracle_params") is not None:
            self.freq_oracle = params.get("freq_oracle")
            self.freq_oracle_params = params.get("freq_oracle_params")
        else:
            self.freq_oracle = "cms"
            self.freq_oracle_params = {}

    def run(self, data):
        # -------------------- Simulating the client-side process --------------------

        sfp_data = []

        hash_families = cms_helper.generate_hash_funcs(self.k, self.m), cms_helper.generate_hash_funcs(self.k_prime,
                                                                                                       self.m_prime)
        client_cms_parameters = [(self.epsilon, self.m), (self.epsilon_prime, self.m_prime)]
        client_sfp = ClientSFP(client_cms_parameters, hash_families, cms_helper.generate_256_hash(),
                               fragment_length=self.fragment_length, max_string_length=self.max_string_length)

        server_cms_parameters = [(self.epsilon, self.k, self.m), (self.epsilon_prime, self.k_prime, self.m_prime)]

        server_sfp = ServerSFP(server_cms_parameters, hash_families, self.threshold,
                               fragment_length=self.fragment_length,
                               max_string_length=self.max_string_length)

        if self.freq_oracle == "cms":
            for item in data:
                sfp_data.append(client_sfp.fragment(item))

            word_estimator, fragment_estimator = server_sfp.generate_cms_estimators(sfp_data)
        else:
            word_estimator, fragment_estimator = client_sfp.fragment_with_oracle(data, self.freq_oracle,
                                                                                 self.freq_oracle_params)

        # -------------------- Simulating the server-side process --------------------

        D, freq_oracle, padding_char = server_sfp.generate_frequencies(word_estimator, fragment_estimator,
                                                                       self.alphabet)

        sfp_freq_data = HeavyHitterList(len(D))

        for i in range(0, len(D)):
            word = D[i].split(padding_char)[0]
            freq = freq_oracle(word)
            if freq >= math.sqrt(len(data)):
                sfp_freq_data.append((word, freq))

        return sfp_freq_data.get_data()
