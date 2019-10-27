import xxhash


class CMSHelper:
    def generate_hash_funcs(self, k, m):
        hash_funcs = []
        for i in range(0, k):
            hash_funcs.append(lambda data: xxhash.xxh64(data, seed=k).intdigest() % m)
        return hash_funcs

cms_helper = CMSHelper()