import math
from scipy.linalg import hadamard
import numpy as np

from algorithms.apple_ldp.cms.client.ClientCMS import ClientCMS

class ServerCMS:
    def __init__(self, dataset, epsilon, k, m, hash_funcs, is_hadamard=False, is_raw_data=False):
        self.k = k
        self.m = m
        self.epsilon = epsilon
        self.hash_funcs = hash_funcs
        self.c = (math.pow(math.e, epsilon / 2) + 1) / (math.pow(math.e, epsilon / 2) - 1)

        # If the data is not privatised then we use client CMS/HCMS to privatise it
        # This wouldn't be used in practice, and is just a helper for simulations
        if is_raw_data:
            client_cms = ClientCMS(self.epsilon, self.hash_funcs, m)
            if is_hadamard:
                dataset = list(map(client_cms.client_hcms, dataset))
            else:
                dataset = list(map(client_cms.client_cms, dataset))

        self.sketch_matrix = self.create_cms_sketch(dataset) if not is_hadamard else self.create_hcms_sketch(dataset)
        self.hash_funcs = hash_funcs

    def freq_oracle(self, data):
        k, m = self.sketch_matrix.shape
        n = len(self.hash_funcs)
        freq_sum = 0
        for i in range(0, k):
            freq_sum += self.sketch_matrix[i][self.hash_funcs[i](data)]
        return (m / (m - 1)) * ((1 / k) * freq_sum - (n / m))

    def create_cms_sketch(self, dataset):
        M = np.zeros((self.k, self.m))
        ones_vector = np.ones(self.m)

        for data in dataset:
            hash_index = data[1]
            M[hash_index] = M[hash_index] + self.k * ((self.c / 2) * data[0] + 0.5 * ones_vector)
        return M

    def create_hcms_sketch(self, dataset):
        M = np.zeros((self.k, self.m))

        for i in range(0, len(dataset)):
            bit_value = dataset[i][0]
            j = dataset[i][1]
            l = dataset[i][2]

            M[j][l] = M[j][l] + self.k * self.c * bit_value

        return np.matmul(M, np.transpose(hadamard(self.m)))
