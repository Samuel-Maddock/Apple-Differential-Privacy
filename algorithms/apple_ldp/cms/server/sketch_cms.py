import math
import numpy as np


def sketch_cms(dataset, epsilon, k, m):
    c = (math.pow(math.e, epsilon / 2) + 1) / (math.pow(math.e, epsilon / 2) - 1)
    x = np.zeros((m, len(dataset)))

    print("Generating sketch vectors...")
    for i in range(0, len(dataset)):
        v = np.array(dataset[i][0])  # Retrieve privatised vector
        ones_vector = np.array([1] * m)
        entry = k * ((c / 2) * v + (1 / 2) * ones_vector)
        x[:, i] = entry

    M = np.zeros((k, m))
    print("Constructing sketch matrix...")
    for i in range(0, len(dataset)):
        for j in range(0, m):
            hash_index = dataset[i][1]
            M[hash_index][j] = M[hash_index][j] + x[:, i][j]
    print("Sketch Matrix Created...")
    return M
