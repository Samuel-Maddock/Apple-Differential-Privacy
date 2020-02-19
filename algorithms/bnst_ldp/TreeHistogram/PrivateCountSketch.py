# A non-static rewrite of the PrivCountSketch.py class ()

# This is mainly used in simulations to test the PrivCountSketch frequency oracle
# The core logic for private count sketch [Charikar-Chen-Farach-Colton 2004]

import numpy as np
import hashlib
from bitarray import bitarray
from bitstring import BitArray
from .DJWRandomizer import randomize
import math


class PrivateCountSketch:
    def __init__(self, l, w, epsilon, use_median=False):
        self.l = l
        self.w = w
        self.epsilon = epsilon
        self.sketch_matrix = np.zeros((l, w))
        self.use_median = use_median

    @staticmethod
    def get_sha256_hash_arr(hashId, dataString):
        message = hashlib.sha256()

        message.update((str(hashId) + dataString).encode("utf8"))

        message_in_bytes = message.digest()

        message_in_bit_array = bitarray(endian='little')
        message_in_bit_array.frombytes(message_in_bytes)

        return message_in_bit_array

    def set_sketch_element(self, data):
        assert (isinstance(data, str) is True), 'Data should be a string'

        hash_id = np.random.randint(0, self.l)
        message_in_bit_array = PrivateCountSketch.get_sha256_hash_arr(hash_id, data)

        h_loc = BitArray(message_in_bit_array[0: int(math.log(self.w, 2))]).uint
        g_val = 2 * message_in_bit_array[int(math.log(self.w, 2))] - 1

        data_vector = np.zeros(self.w)
        data_vector[h_loc] = g_val

        privatized_vec = randomize(data_vector)

        self.sketch_matrix[hash_id] += (privatized_vec * self.epsilon * self.l)

    def write_sketch(self, sketch_location):
        np.save(sketch_location, self.sketch_matrix)

    def read_sketch(self, sketch_location):
        self.sketch_matrix = np.load(sketch_location)

    def get_freq_estimate(self, data):
        assert (isinstance(data, str) is True), 'Data should be a string'

        weak_freq_estimates = np.zeros(self.l)
        for hashId in range(0, self.l):
            message_in_bit_array = PrivateCountSketch.get_sha256_hash_arr(hashId, data)

            h_loc = BitArray(message_in_bit_array[0: int(math.log(self.w, 2))]).uint
            g_val = 2 * message_in_bit_array[int(math.log(self.w, 2))] - 1
            weak_freq_estimates[hashId] = g_val * self.sketch_matrix[hashId, h_loc]

        if self.use_median:
            return np.median(weak_freq_estimates)
        else:
            return np.mean(weak_freq_estimates)