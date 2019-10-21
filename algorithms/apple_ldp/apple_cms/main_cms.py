import xxhash
import numpy
from algorithms.apple_ldp.apple_cms.client.client_cms import client_cms
from algorithms.apple_ldp.apple_cms.server.sketch_cms import sketch_cms
from algorithms.apple_ldp.apple_cms.server.server_cms import server_cms

def generate_hash_funcs(k, m):
    hash_funcs = []
    for i in range (0,k):
        hash_funcs.append(lambda data: xxhash.xxh64(data, seed=k).intdigest() % m)
    return hash_funcs


m = 65536
k = 1024
epsilon = 4

hash_funcs = generate_hash_funcs(k, m)

d = "Test String"
dataset = []

for i in range(0,1000):
    dataset.append(client_cms(epsilon, d, hash_funcs, m))

M = sketch_cms(dataset, epsilon, k, m)

freq_estimate = server_cms(d, M, hash_funcs)
print(freq_estimate) # The freq estimate should be approximately 1000 (Since our dataset is 1000 of the same elements)