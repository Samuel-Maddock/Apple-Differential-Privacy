# Server side component of Count sketch, contains distribution and aggregation logic
import pandas as pd
import numpy as np
import math
import uuid
import itertools

from algorithms.bnst_ldp.TreeHistogram.PrivateCountSketch import PrivateCountSketch
from algorithms.bnst_ldp.Bitstogram.Hashtogram import Hashtogram
from algorithms.bnst_ldp.Bitstogram.ExplicitHist import ExplicitHist
from algorithms.apple_ldp.cms.server.ServerCMS import ServerCMS
from collections import deque, Counter

class TreeHistogram:
    def __init__(self, l, w, epsilon, num_n_grams, gram_length, threshold, alphabet):
        self.l = l
        self.w = w
        self.epsilon = epsilon
        self.num_n_grams = num_n_grams  # Number of N-grams
        self.gram_length = gram_length  # Gram length
        self.threshold = threshold
        self.empty_char = "*"

        # TODO: Test this
        if "*" in alphabet:
            alphabet.remove(self.empty_char)

        self.alphabet = alphabet

    def __choose_random_n_gram_prefix(self, word, N):
        assert len(word) % N == 0, 'Word = ' + word + ' is not of correct length'
        random_start_index = np.random.randint(0, len(word) / N) * N
        random_prefix_word = word[0:random_start_index + N] + self.empty_char * (
                    self.gram_length * self.num_n_grams - len(word[0:random_start_index + N]))
        return random_prefix_word

    def __gen_english_n_grams(self, alphabet):
        n_gram_arr = itertools.product(alphabet, repeat=self.gram_length)
        n_gram_arr = map(lambda x: "".join(x), n_gram_arr)
        return list(n_gram_arr)

    # wordFrequency: The data file as a dataframe with the two columns ['word', 'trueFrequency']
    # configFileName: File to dump the configuration parameters. Include expt info in the filename
    # expResultFile: File to dump the experiment results as a .csv file

    def run_server_side(self, word_frequency):
        priv_count_sketch = PrivateCountSketch(self.l, self.w, self.epsilon)

        for index, row in word_frequency.iterrows():
            for i in range(row['trueFrequency']):
                priv_count_sketch.set_sketch_element(row['word'])

        priv_frequency = [0] * len(word_frequency)
        priv_error = [0] * len(word_frequency)
        for i, word in enumerate(word_frequency['word']):
            priv_frequency[i] = int(priv_count_sketch.freq_oracle(word))
            priv_error[i] = int(priv_frequency[i] - word_frequency['trueFrequency'][i])

        word_frequency['privateFreq_run_freq'] = priv_frequency
        word_frequency['privateFreq_run_error'] = priv_error

        print(word_frequency)
        return word_frequency

    def run_server_side_word_discovery(self, data, freq_oracle=None, freq_oracle_params=None):
        word_length = self.num_n_grams * self.gram_length
        word_frequency = pd.DataFrame(list(dict(Counter(data)).items()), columns=["word", "trueFrequency"])
        pres_rec_df = pd.DataFrame(['NumOfWords', 'Precision', 'Recall'], columns=['Measure'])

        # Simulating client-side
            # PrivateCountSketch is the standard freq oracle for TreeHistogram
            # Can also provide other frequency oracles for simulation results

        if freq_oracle is None or freq_oracle_params is None:
            fragment_estimator = PrivateCountSketch(self.l, self.w, self.epsilon, use_median=True)
            word_estimator = PrivateCountSketch(self.l, self.w, self.epsilon)

            for index, row in word_frequency.iterrows():
                for i in range(row['trueFrequency']):
                    current_word = row['word']
                    word_estimator.set_sketch_element(current_word)

                    if len(current_word) <= word_length:
                        current_word += self.empty_char * (word_length - len(current_word))
                    else:
                        current_word = current_word[:word_length]

                    word_to_send = self.__choose_random_n_gram_prefix(current_word, self.gram_length)

                    fragment_estimator.set_sketch_element(word_to_send)
        else:
            params = freq_oracle_params
            freq_oracles = {
                "priv_count_sketch": lambda dataset: PrivateCountSketch(**params, data=dataset),
                "priv_count_sketch_median": lambda dataset: PrivateCountSketch(**params, data=dataset, use_median=True),
                "explicithist": lambda dataset: ExplicitHist(dataset, **params),
                "hashtogram": lambda dataset: Hashtogram(dataset, **params),
                "hashtogram_median": lambda dataset: Hashtogram(dataset, **params, use_median=True),
                "cms": lambda dataset: ServerCMS(dataset, **params, is_raw_data=True),
                "hcms": lambda dataset: ServerCMS(dataset, **params, is_hadamard=True, is_raw_data=True)
            }

            word_estimator = freq_oracles.get(freq_oracle)(data)
            fragments = list(map(lambda word: self.__choose_random_n_gram_prefix(word, self.gram_length), data))
            fragment_estimator = freq_oracles.get(freq_oracle)(fragments)

        # ------------------ Server-side Frequency estimation section ------------------
        scaling_factor = self.num_n_grams
        n_gram_set = self.__gen_english_n_grams(self.alphabet)
        list_n_grams = [s + self.empty_char * (word_length - len(s)) for s in n_gram_set]
        word_queue = deque(list_n_grams)
        noisy_frequencies = {}

        while word_queue.__len__() != 0:
            current_prefix = word_queue.popleft()
            current_prefix_after_stripping_empty = current_prefix.replace(self.empty_char, '')
            freq_for_current_prefix = int(fragment_estimator.freq_oracle(current_prefix))

            if freq_for_current_prefix < self.threshold:
                continue

            if len(current_prefix_after_stripping_empty) == word_length:
                noisy_frequencies[current_prefix_after_stripping_empty] = freq_for_current_prefix
                continue

            for gram in n_gram_set:
                toAdd = current_prefix_after_stripping_empty + gram + self.empty_char * (
                        word_length - (len(current_prefix_after_stripping_empty) + self.gram_length))
                word_queue.append(toAdd)

        TP = 0.0
        FN = 0.0
        priv_frequency = [0] * len(word_frequency)

        for index, row in word_frequency.iterrows():
            word = row['word']
            true_frequency = row['trueFrequency']
            if word not in list(noisy_frequencies.keys()):
                priv_frequency[index] = 0
                if true_frequency > self.threshold:
                    FN += 1
            else:
                priv_frequency[index] = noisy_frequencies[word]
                if true_frequency > self.threshold:
                    TP += 1

        FP = noisy_frequencies.__len__() - TP
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)

        word_frequency['privateFreq_run'] = priv_frequency
        pres_rec_df['Run'] = [word_frequency.__len__(), precision, recall]

        # Reapproximate frequencies based on the minimum of the estimates of fragment frequency vs whole dataset frequenc
        heavy_hitters = {}
        for key, value in noisy_frequencies.items():
            freq = word_estimator.freq_oracle(key)
            if min(value,freq) >= 0:
                heavy_hitters[key] = max(value,freq)

        return list(heavy_hitters.items())
