import numpy as np

from algorithms.apple_ldp.sfp.server.ServerSFP import ServerSFP
from algorithms.apple_ldp.sfp.client.ClientSFP import ClientSFP
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from algorithms.apple_ldp.sfp.HeavyHitterList import HeavyHitterList
from collections import Counter


class SFPSimulation:
    def __init__(self, params):
        self.epsilon = params["epsilon"]
        self.m = params["m"]
        self.k = params["k"]
        self.epsilon_prime = params["epsilon_prime"]
        self.m_prime = params["m_prime"]
        self.k_prime = params["k_prime"]
        self.threshold = params["threshold"]
        self.alphabet = params["alphabet"]

    def run(self, data):
        # -------------------- Simulating the client-side process --------------------

        sfp_data = []

        hash_families = cms_helper.generate_hash_funcs(self.k, self.m), cms_helper.generate_hash_funcs(self.k_prime, self.m_prime)
        client_sfp = ClientSFP([(self.epsilon, self.m), (self.epsilon_prime, self.m_prime)], hash_families, cms_helper.generate_256_hash())

        for word in data:
            sfp_data.append(client_sfp.fragment(word))  # Client_SFP the word and add it to the sfp_data

        # -------------------- Simulating the server-side process --------------------

        server_sfp = ServerSFP([(self.epsilon, self.k, self.m), (self.epsilon_prime, self.k_prime, self.m_prime)], hash_families, self.threshold)
        D, freq_oracle = server_sfp.generate_frequencies(sfp_data, self.alphabet)

        sfp_freq_data = HeavyHitterList(len(D))

        for i in range(0, len(D)):
            sfp_freq_data.append((D[i], freq_oracle(D[i])))

        return sfp_freq_data.get_data()


