class ServerCMS:
    def __init__(self, sketch_matrix, hash_funcs):
        self.sketch_matrix = sketch_matrix
        self.hash_funcs = hash_funcs

    def estimate_freq(self, data):
        k, m = self.sketch_matrix.shape
        n = len(self.hash_funcs)
        freq_sum = 0
        for i in range(0, k):
            freq_sum += self.sketch_matrix[i][self.hash_funcs[i](data)]
        return (m / (m - 1)) * ((1 / k) * freq_sum - (n / m))
