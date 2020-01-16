# Server side component of Count sketch, contains distribution and aggregation logic
import pandas as pd
import numpy as np
import math
import uuid

from algorithms.bnst_ldp.TreeHistogram.PrivateCountSketch import PrivateCountSketch
from collections import deque


class TreeHistogram():
    def __init__(self, l, w, epsilon, num_n_grams, gram_length, threshold):
        self.l = l
        self.w = w
        self.epsilon = epsilon
        self.num_n_grams = num_n_grams  # Number of N-grams
        self.gram_length = gram_length  # Gram length
        self.threshold = threshold
        self.empty_char = "?"

    def checkArrayCounterMaxReached(self, arrayOfCounters):
        if arrayOfCounters[0] == 3:
            return True
        return False

    def incrementArray(self, arrayOfCounters):
        arrayOfCounters[-1] += 1
        for i in range(len(arrayOfCounters) - 1, 0, -1):
            if arrayOfCounters[i] == 3:
                arrayOfCounters[i] = 0
                arrayOfCounters[i - 1] += 1

    def _choose_random_n_gram_prefix(self, word, N):
        assert len(word) % N == 0, 'Word = ' + word + ' is not of correct length'
        random_start_index = np.random.randint(0, len(word) / N) * N
        random_prefix_word = word[0:random_start_index + N] + self.empty_char * (
                    self.gram_length * self.num_n_grams - len(word[0:random_start_index + N]))
        return random_prefix_word

    def _gen_english_n_grams(self, N):
        gram_dict = [''] * (int(math.pow(3, N)))
        counter = 0
        word_length = self.gram_length
        array_of_counters = [0] * word_length
        while(self.checkArrayCounterMaxReached(array_of_counters) == False):
            for x in array_of_counters:
                gram_dict[counter] += chr(97 + x)
            counter += 1
            self.incrementArray(array_of_counters)
        return gram_dict

    # wordFrequency: The data file as a dataframe with the two columns ['word', 'trueFrequency']
    # configFileName: File to dump the configuration parameters. Include expt info in the filename
    # expResultFile: File to dump the experiment results as a .csv file

    def runServerSide(self, word_frequency):

        priv_count_sketch = PrivateCountSketch(self.l, self.w, self.epsilon)

        for index, row in word_frequency.iterrows():
            for i in range(row['trueFrequency']):
                priv_count_sketch.set_sketch_element(row['word'])

        priv_frequency = [0] * len(word_frequency)
        priv_error = [0] * len(word_frequency)
        for i, word in enumerate(word_frequency['word']):
            priv_frequency[i] = int(priv_count_sketch.get_freq_estimate(word))
            priv_error[i] = int(priv_frequency[i] - word_frequency['trueFrequency'][i])

        word_frequency['privateFreq_run_freq'] = priv_frequency
        word_frequency['privateFreq_run_error'] = priv_error

        print(word_frequency)
        return word_frequency

    def runServerSideWordDiscovery(self, word_frequency):

        word_length = self.num_n_grams * self.gram_length
        n_gram_set = self._gen_english_n_grams(self.gram_length)

        pres_rec_df = pd.DataFrame(['NumOfWords', 'Precision', 'Recall'], columns=['Measure'])

        priv_count_sketch = PrivateCountSketch(self.l, self.w, self.epsilon, use_median=True)
        main_count_sketch = PrivateCountSketch(self.l, self.w, self.epsilon)

        # Simulating client-side
        for index, row in word_frequency.iterrows():
            for i in range(row['trueFrequency']):

                current_word = row['word']
                main_count_sketch.set_sketch_element(current_word)

                if len(current_word) <= word_length:
                    current_word += self.empty_char * (word_length - len(current_word))
                else:
                    current_word = current_word[:word_length]

                word_to_send = self._choose_random_n_gram_prefix(current_word, self.gram_length)

                priv_count_sketch.set_sketch_element(word_to_send)

        # Server-side Frequency estimation section
        scaling_factor = self.num_n_grams
        list_n_grams = self._gen_english_n_grams(self.gram_length)
        list_n_grams = [s + self.empty_char * (word_length - len(s)) for s in list_n_grams]
        word_queue = deque(list_n_grams)
        noisy_frequencies = {}

        while (word_queue.__len__() != 0):
            current_prefix = word_queue.popleft()
            current_prefix_after_stripping_empty = current_prefix.replace(self.empty_char, '')
            freq_for_current_prefix = int(priv_count_sketch.get_freq_estimate(current_prefix) * scaling_factor)

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
            freq = main_count_sketch.get_freq_estimate(key)
            if min(value,freq) >= 0:
                heavy_hitters[key] = min(value,freq)

        #print(heavy_hitters)
        #return list(noisy_frequencies.items())

        return list(heavy_hitters.items())
