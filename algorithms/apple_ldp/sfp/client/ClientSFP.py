import numpy as np
from algorithms.apple_ldp.cms.client.ClientCMS import ClientCMS


class ClientSFP:
    def __init__(self, cms_params, hash_families, hash_256):
        epsilon, m = cms_params[0]
        epsilon_prime, m_prime = cms_params[1]
        self.hash_256 = hash_256
        self.word_cms = ClientCMS(epsilon, hash_families[0], m)
        self.fragment_cms = ClientCMS(epsilon_prime, hash_families[1], m_prime)

    def fragment(self, string):
        odd_numbers = np.arange(1, len(string), step=2)
        l = np.random.choice(odd_numbers)
        r = str(self.hash_256(string)) + string[l-1: l + 1]
        return self.fragment_cms.client_cms(r), self.word_cms.client_cms(string), l
