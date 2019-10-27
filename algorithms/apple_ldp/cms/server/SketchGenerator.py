import math
from scipy.linalg import hadamard
import numpy as np


class SketchGenerator:
    def __init__(self, epsilon, k, m):
        self.k = k
        self.m = m
        self.epsilon = epsilon
        self.c = (math.pow(math.e, epsilon / 2) + 1) / (math.pow(math.e, epsilon / 2) - 1)
        self.transposed_hadamard = np.transpose(hadamard(self.m)) # Generate here to speed up sketch creation

    def create_cms_sketch(self, dataset):
        x = np.zeros((self.m, len(dataset)))

        print("Generating sketch vectors...")
        for i in range(0, len(dataset)):
            v = np.array(dataset[i][0])  # Retrieve privatised vector
            ones_vector = np.array([1] * self.m)
            entry = self.k * ((self.c / 2) * v + (1 / 2) * ones_vector)
            x[:, i] = entry

        M = np.zeros((self.k, self.m))
        print("Constructing sketch matrix...")
        for i in range(0, len(dataset)):
            for j in range(0, self.m):
                hash_index = dataset[i][1]
                M[hash_index][j] = M[hash_index][j] + x[:, i][j]
        print("Sketch Matrix Created...")
        return M

    def create_hcms_sketch(self, dataset):
        print("Generating Hadamard Sketch Matrix...")
        x = np.zeros(len(dataset))
        M = np.zeros((self.k, self.m))

        for i in range(0, len(dataset)):
            bit_value = dataset[i][0]
            j = dataset[i][1]
            l = dataset[i][2]

            x[i] = self.k * self.c * bit_value
            M[j][l] = M[j][l] + x[i]

        print("Sketch Matrix Created")
        return np.matmul(M, np.transpose(hadamard(self.m)))
