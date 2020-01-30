import numpy as np

from algorithms.apple_ldp.sfp.server.ServerSFP import ServerSFP
from algorithms.apple_ldp.sfp.client.ClientSFP import ClientSFP
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from algorithms.apple_ldp.sfp.HeavyHitterList import HeavyHitterList

from simulations.heavy_hitters.helpers.HeavyHitterSimulation import HeavyHitterSimulation

from collections import Counter


class SFPSimulation(HeavyHitterSimulation):
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

    def run(self, data):
        # -------------------- Simulating the client-side process --------------------

        sfp_data = []

        hash_families = cms_helper.generate_hash_funcs(self.k, self.m), cms_helper.generate_hash_funcs(self.k_prime, self.m_prime)
        client_cms_parameters = [(self.epsilon, self.m), (self.epsilon_prime, self.m_prime)]
        client_sfp = ClientSFP(client_cms_parameters, hash_families, cms_helper.generate_256_hash(), fragment_length=self.fragment_length, max_string_length=self.max_string_length)

        for word in data:
            sfp_data.append(client_sfp.fragment(word))  # Client_SFP the word and add it to the sfp_data

        # -------------------- Simulating the server-side process --------------------
        cms_parameters = [(self.epsilon, self.k, self.m), (self.epsilon_prime, self.k_prime, self.m_prime)]
        server_sfp = ServerSFP(cms_parameters, hash_families, self.threshold, fragment_length=self.fragment_length, max_string_length=self.max_string_length)
        D, freq_oracle = server_sfp.generate_frequencies(sfp_data, self.alphabet)

        sfp_freq_data = HeavyHitterList(len(D))

        for i in range(0, len(D)):
            sfp_freq_data.append((D[i], freq_oracle(D[i])))

        return sfp_freq_data.get_data()

