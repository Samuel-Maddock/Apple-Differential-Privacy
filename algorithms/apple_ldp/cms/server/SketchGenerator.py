import math
from scipy.linalg import hadamard
import numpy as np


class SketchGenerator:
    def __init__(self, epsilon, k, m):
        self.k = k
        self.m = m
        self.epsilon = epsilon
        self.c = (math.pow(math.e, epsilon / 2) + 1) / (math.pow(math.e, epsilon / 2) - 1)

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
