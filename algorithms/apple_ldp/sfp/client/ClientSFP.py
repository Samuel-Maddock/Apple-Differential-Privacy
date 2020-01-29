import numpy as np
from algorithms.apple_ldp.cms.client.ClientCMS import ClientCMS
from collections import namedtuple

class ClientSFP:
    def __init__(self, cms_params, hash_families, hash_256, fragment_length=2, max_string_length=6, padding_char="*"):
        Parameters = namedtuple("Parameters", ["epsilon", "m"])
        self.word_parameters = Parameters(*cms_params[0])
        self.fragment_parameters = Parameters(*cms_params[1])

        self.hash_256 = hash_256
        self.word_cms = ClientCMS(self.word_parameters.epsilon, hash_families[0], self.word_parameters.m)
        self.fragment_cms = ClientCMS(self.fragment_parameters.epsilon, hash_families[1], self.fragment_parameters.m)
        self.max_string_length = max_string_length
        self.padding_char = padding_char
        self.fragment_length = fragment_length

    def fragment(self, string):

        # Pad strings that are smaller than some arbitrary max value
        if len(string) < self.max_string_length:
            string += (self.max_string_length - len(string)) * self.padding_char
        elif len(string) > self.max_string_length:
            string = string[0:self.max_string_length]

        fragment_indices = np.arange(1, len(string), step=self.fragment_length)
        l = np.random.choice(fragment_indices)
        r = str(self.hash_256(string)) + "_" + string[l-1: l + (self.fragment_length-1)]
        return self.fragment_cms.client_cms(r), self.word_cms.client_cms(string), l
