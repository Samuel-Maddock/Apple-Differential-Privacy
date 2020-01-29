from algorithms.apple_ldp.cms.server.ServerCMS import ServerCMS
from algorithms.apple_ldp.cms.server.SketchGenerator import SketchGenerator
from algorithms.apple_ldp.sfp.HeavyHitterList import HeavyHitterList
from collections import namedtuple
from collections import defaultdict
import string
import numpy as np
import re
import itertools


class ServerSFP:
    def __init__(self, cms_params, hash_families, threshold, fragment_length=2, max_string_length=6, padding_char="*"):
        Parameters = namedtuple("Parameters", ["epsilon", "k", "m"])
        self.word_parameters = Parameters(*cms_params[0])
        self.fragment_parameters = Parameters(*cms_params[1])
        self.word_hash_functions, self.fragment_hash_functions = hash_families
        self.threshold = threshold
        self.fragment_length = fragment_length
        self.max_string_length = max_string_length
        self.padding_char = padding_char

    def __create_fragment_estimators(self, data, indexes):
        estimator_dict = {}
        dict_vals = defaultdict(list)

        for index_data_pair in zip(indexes, data):
            dict_vals[index_data_pair[0]].append(index_data_pair[1])

        for l in range(0, 10):
            if dict_vals.get(l) is not None:
                M = SketchGenerator(*self.fragment_parameters).create_cms_sketch(dict_vals.get(l))
                estimator_dict[l] = ServerCMS(M, self.fragment_hash_functions).estimate_freq
        return estimator_dict

    def __generate_frequent_fragments(self, fragments, estimators):
        for estimator in estimators:
            frequencies = []
            for fragment in fragments:
                frequency = estimator[1](fragment)
                frequencies.append(frequency)

    def __split_fragment(self, fragment):
        fragment_split = fragment.split("_", 1)
        return fragment_split[0], fragment_split[1]

    def generate_frequencies(self, sfp_data, alphabet):
        alpha_list, beta_list, index_list = list(zip(*sfp_data))

        word_sketch_generator = SketchGenerator(*self.word_parameters)
        M = word_sketch_generator.create_cms_sketch(beta_list)
        freq_oracle = ServerCMS(M, self.word_hash_functions).estimate_freq

        estimator_list = self.__create_fragment_estimators(alpha_list, index_list)

        D = []
        fragments = []
        frequency_dict = defaultdict(lambda: HeavyHitterList(self.threshold))

        fragments = list(map(lambda x: x[0] + x[1], itertools.product(alphabet, alphabet)))

        for i in range(0, 256):
            for fragment in fragments:
                fragment = str(i) + "_" + str(fragment)
                for estimator in estimator_list.items():
                    fragment_freq_pair = fragment, estimator[1](fragment)
                    frequency_dict[estimator[0]].append(fragment_freq_pair)

        hash_table = defaultdict(lambda: defaultdict(list))

        fragment_indices = np.arange(1, self.max_string_length, step=self.fragment_length)
        for l in fragment_indices:
            fragments, frequencies = zip(*frequency_dict.get(l).get_data())
            for fragment in fragments:
                key, value = self.__split_fragment(fragment)
                hash_table[key][l].append(value)

        for dictionary in hash_table.values():
            fragment_list = list(dictionary.values())
            if len(fragment_list) == int(self.max_string_length / self.fragment_length):
                D += list(map(lambda x: str().join(x).split(self.padding_char)[0], itertools.product(*fragment_list)))

        return D, freq_oracle
