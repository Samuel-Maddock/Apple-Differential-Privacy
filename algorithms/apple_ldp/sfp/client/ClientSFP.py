import numpy as np
from algorithms.apple_ldp.cms.client.ClientCMS import ClientCMS
from collections import namedtuple
from collections import defaultdict
from algorithms.bnst_ldp.Bitstogram.Hashtogram import Hashtogram
from algorithms.bnst_ldp.Bitstogram.ExplicitHist import ExplicitHist
from algorithms.bnst_ldp.TreeHistogram.PrivateCountSketch import PrivateCountSketch
from algorithms.core_ldp.FreqOracle import FreqOracle

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

        if max_string_length is None:
            self.max_string_length = 6
        if fragment_length is None:
            self.fragment_length = 2

    # Used to create SFP fragments
    # Generic method used by other frequency oracles
    def _create_fragment(self, string):
        # Pad strings that are smaller than some arbitrary max value
        if len(string) < self.max_string_length:
            string += (self.max_string_length - len(string)) * self.padding_char
        elif len(string) > self.max_string_length:
            string = string[0:self.max_string_length]

        fragment_indices = np.arange(0, len(string), step=self.fragment_length)
        l = np.random.choice(fragment_indices)
        r = str(self.hash_256(string)) + "_" + string[l: l + (self.fragment_length)]

        return r, string, l

    # Combines client-side + server-side hashtogram to produce estimators for hashtogram SFP
    def fragment_with_oracle(self, data, oracle="", params=None):

        freq_oracles = {
            "priv_count_sketch": lambda dataset: PrivateCountSketch(**params, data=dataset),
            "priv_count_sketch_median": lambda dataset: PrivateCountSketch(**params, data=dataset, use_median=True),
            "hashtogram": lambda dataset: Hashtogram(dataset, **params),
            "hashtogram_median": lambda dataset: Hashtogram(dataset, **params, use_median=True)
        }

        fragment_data = list(map(lambda x: self._create_fragment(x), data))
        words = list(zip(*fragment_data))[1]
        estimator_dict = {}
        dict_vals = defaultdict(list)

        for data in fragment_data:
            dict_vals[data[2]].append(data[0])

        for l in range(0, self.max_string_length):
            if dict_vals.get(l) is not None:
                estimator_dict[l] = freq_oracles.get(oracle)(dict_vals.get(l)).freq_oracle

        word_estimator = freq_oracles.get(oracle)(words).freq_oracle

        return word_estimator, estimator_dict

    # The SFP Client-side algorithm for CMS/HCMS (The original outlined in the apple paper)
    def fragment(self, string):
        r, string, l = self._create_fragment(string)
        return self.fragment_cms.client_cms(r), self.word_cms.client_cms(string), l