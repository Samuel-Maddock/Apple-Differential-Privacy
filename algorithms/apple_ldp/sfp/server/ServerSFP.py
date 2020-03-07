from algorithms.apple_ldp.cms.server.ServerCMS import ServerCMS
from collections import namedtuple
from collections import defaultdict
from collections import Counter

import numpy as np
import itertools
import pathos.pools as pp


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

        if max_string_length is None:
            self.max_string_length = 6
        if fragment_length is None:
            self.fragment_length = 2

    def __create_fragment_estimators(self, data, indexes):
        estimator_dict = {}
        dict_vals = defaultdict(list)

        for index_data_pair in zip(indexes, data):
            dict_vals[index_data_pair[0]].append(index_data_pair[1])

        for l in range(0, self.max_string_length):
            if dict_vals.get(l) is not None:
                estimator_dict[l] = ServerCMS(dict_vals.get(l), *self.fragment_parameters,
                                              self.fragment_hash_functions).freq_oracle

        return estimator_dict

    def __split_fragment(self, fragment):
        fragment_split = fragment.split("_", 1)
        return fragment_split[0], fragment_split[1]

    def __generate_fragments(self, alphabet):
        fragment_arr = itertools.product(alphabet, repeat=self.fragment_length)
        fragment_arr = map(lambda x: "".join(x), fragment_arr)
        fragment_arr = itertools.product(map(str, range(0, 256)), "_", fragment_arr)
        return list(map(lambda x: "".join(x), fragment_arr))

    def generate_cms_estimators(self, sfp_data):
        alpha_list, beta_list, index_list = list(zip(*sfp_data))
        word_estimator = ServerCMS(beta_list, *self.word_parameters, self.word_hash_functions).freq_oracle
        fragment_estimators = self.__create_fragment_estimators(alpha_list, index_list)

        return word_estimator, fragment_estimators

    def generate_frequencies(self, word_estimator, fragment_estimators, alphabet):
        alphabet.add(self.padding_char)

        freq_oracle = word_estimator
        fragment_estimators = fragment_estimators

        D = []

        fragments = self.__generate_fragments(alphabet)

        frequency_dict = defaultdict(lambda: Counter())

        # Computationally checking the frequency estimates of every possible fragment is slow
        # We use python multithreading to make this quicker
        # We use the pathos library since the standard multiprocessing library doesn't allow pool maps in class methods

        pool = pp.ProcessPool()

        def estimate_fragments(key, frag_estimator):
            frag_dict = dict()

            for frag in fragments:
                frag_dict[frag] = frag_estimator(frag)

            return key, Counter(frag_dict)

        # estimate_fragments = lambda key, frag_estimator: (key, Counter({k:v for k,v in map(lambda x: (x, frag_estimator(x)), fragments)}))

        pool_map = pool.uimap(estimate_fragments, fragment_estimators.keys(), fragment_estimators.values())

        for item in pool_map:
            frequency_dict[item[0]] = item[1]

        hash_table = defaultdict(lambda: defaultdict(list))

        fragment_indices = np.arange(0, self.max_string_length, step=self.fragment_length)

        for l in fragment_indices:
            fragments = frequency_dict.get(l).most_common(self.threshold)
            for fragment in fragments:
                key, value = self.__split_fragment(fragment[0])
                hash_table[key][l].append(value)

        for dictionary in hash_table.values():
            fragment_list = list(dictionary.values())

            if len(dictionary.keys()) == self.max_string_length / self.fragment_length:
                D += list(map(lambda x: str().join(x), itertools.product(*fragment_list)))

        return D, freq_oracle, self.padding_char
