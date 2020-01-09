import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from algorithms.apple_ldp.cms.client.ClientCMS import ClientCMS
from algorithms.apple_ldp.cms.server.SketchGenerator import SketchGenerator
from algorithms.apple_ldp.cms.server.ServerCMS import ServerCMS
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from collections import Counter

# This is an example file showing you how to use the CMS algorithm
# For actual plot generation/simulation usage, you should use the CMSSimulation.py
    # CMSSimulation.py wraps the logic in this file in a cleaner to use class

# -------------------- Parameters for simulation --------------------
m = 2048
k = 1024
epsilon = 4

N = 10000
mu = 10
sd = 3

# -------------------- Simulating the client-side process --------------------

hash_funcs = cms_helper.generate_hash_funcs(k, m)

data = np.random.normal(mu,sd,N).astype(int)
ldp_data = []

bins = np.arange(start=min(data), stop = max(data) + 1)
fig, axs = plt.subplots(3)

client_cms = ClientCMS(epsilon, hash_funcs, m)
sketch_generator = SketchGenerator(epsilon, k, m)

print("Sampling data from the clients...")
for i in range(0,N):
    ldp_data.append(client_cms.client_cms(data[i]))

# -------------------- Simulating the server-side process --------------------

M = sketch_generator.create_cms_sketch(ldp_data)

server_cms = ServerCMS(M, hash_funcs)

print("Estimating frequencies from sketch matrix...")
ldp_freq = np.empty(len(bins))
ldp_plot_data = np.empty(len(bins))
for key in bins:
    ldp_freq[key-1] = server_cms.estimate_freq(key)
    ldp_plot_data = np.append(ldp_plot_data, [key]*int(ldp_freq[key-1]))

# -------------------- Calculating Error --------------------

original_freq_data = dict(Counter(data.tolist()))
ldp_freq_data = dict(Counter(ldp_plot_data.tolist()))

max_error = 0
avg_error = 0
max_bin = 0

for bin in bins:
    error = abs(ldp_freq_data.get(bin, 0)-original_freq_data.get(bin, 0))
    if max_error < error:
        max_error = error
        max_bin = bin
    avg_error += error

avg_error = avg_error/len(bins)

print("Average Error: " + str(avg_error))
print("Max Error: " + str(max_error) + " occurs at bin " + str(max_bin))

# -------------------- Plotting the data --------------------
print("Plotting data...")

# Plotting a distplot of our integer data sampled from a normal dist
sns.distplot(data, bins=bins, ax=axs[0], hist_kws={'ec': "black"})
axs[0].set_title("Count Mean Sketch (CMS) \n Integer data sampled from a Normal distribution \n $N=${}, Sampled from $N({}, {})$".format(N, mu, sd*sd))

# Plotting a distplot of the data produced from the CMS algorithm
sns.distplot(ldp_plot_data, bins=bins, ax=axs[1], color='r', hist_kws={'ec': "black"})
axs[1].set_title("LDP CMS data produced from the normal sample \n $\epsilon=${}, $m=${}, $k=${}".format(epsilon, m, k))

# Plotting both kde's from above for comparison
sns.distplot(ldp_plot_data, hist=False, bins=bins, ax=axs[2], color='r')
sns.distplot(data, bins=bins, hist=False, ax=axs[2])

fig.tight_layout()
plt.savefig("cms.png")
plt.show()
print("Plot Displayed !")
