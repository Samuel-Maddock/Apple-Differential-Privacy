import xxhash
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from algorithms.apple_ldp.apple_cms.client.client_cms import client_cms
from algorithms.apple_ldp.apple_cms.server.sketch_cms import sketch_cms
from algorithms.apple_ldp.apple_cms.server.server_cms import server_cms

def generate_hash_funcs(k, m):
    hash_funcs = []
    for i in range (0,k):
        hash_funcs.append(lambda data: xxhash.xxh64(data, seed=k).intdigest() % m)
    return hash_funcs


m = 10000
k = 1024
epsilon = 4

hash_funcs = generate_hash_funcs(k, m)

ldp_data = []
data = np.random.normal(10,3,5000).astype(int)
bins = np.arange(start=min(data), stop = max(data) + 1)
fig, axs = plt.subplots(2)

sns.distplot(data, bins=bins, ax=axs[0])
axs[0].set_title("Integer data sampled from a normal distribution")

print("Sampling data from the clients...")
for i in range(0,5000):
    ldp_data.append(client_cms(epsilon, data[i], hash_funcs, m))

M = sketch_cms(ldp_data, epsilon, k, m)

print(server_cms(np.int64(10), M, hash_funcs))

print("Estimating frequencies from sketch matrix...")
ldp_freq = np.empty(len(bins))
ldp_plot_data = np.empty(len(bins))
for key in bins:
    ldp_freq[key-1] = server_cms(key, M, hash_funcs)
    ldp_plot_data = np.append(ldp_plot_data, [key]*int(ldp_freq[key-1]))
print("Plotting data...")

sns.distplot(ldp_plot_data, bins=bins, ax=axs[1], color='r')
axs[1].set_title("LDP CMS data produced from the normal sample")
plt.show()

print("Plot Displayed !")
print(ldp_freq)
