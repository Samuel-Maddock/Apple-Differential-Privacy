import xxhash


class CMSHelper:
    def generate_hash_funcs(self, k, m):
        hash_funcs = []
        for i in range(0, k):
            hash_funcs.append(self.generate_hash(m, i))
        return hash_funcs

    def generate_256_hash(self):
        return lambda data: xxhash.xxh64(data, seed=10).intdigest() % 256

    def generate_hash(self, m, seed):
        return lambda data: xxhash.xxh64(str(data), seed=seed).intdigest() % m

cms_helper = CMSHelper()