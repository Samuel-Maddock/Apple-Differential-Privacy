from algorithms.apple_ldp.sfp.client.ClientSFP import ClientSFP
from algorithms.apple_ldp.sfp.server.ServerSFP import ServerSFP
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from algorithms.apple_ldp.sfp.HeavyHitterList import HeavyHitterList
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import itertools
import string
import time

# -------------------- Parameters for simulation --------------------

m = 2048
k = 1024  # We use k = k_prime and m = m_prime for our simulation

epsilon = 2
epsilon_prime = 6
threshold = 30

N = 10000
alphabet = list("abc")
word_size = 10
word_sample_size = 10

# -------------------- Generating Test Data --------------------

# We generate all possible word_size character strings from our alphabet
# We then sample from this randomly to choose word_sample_size words
# We then use these words to sample our data from

print("SFP Word Count Simulation...")
start_time = time.time()

alphabet_list = []
for i in range(0, word_size):
    alphabet_list.append(alphabet)

# Form all possible strings of length word_size from our given alphabet
strings = list(set(map(lambda x: str().join(x), itertools.product(*alphabet_list))))

def generate_words(n):
    words = set()
    for i in range(0, n):
        words.add(np.random.choice(strings))
    return list(words)


words = generate_words(word_sample_size)

print("Test data generated in: " + str(time.time()-start_time) + " seconds")
start_time = time.time()

# -------------------- Simulating the client-side process --------------------

dataset = []  # Dataset of words formed from our alphabet
sfp_data = []  # Client-side data returned from SFP

hash_families = cms_helper.generate_hash_funcs(k, m), cms_helper.generate_hash_funcs(k, m)
client_sfp = ClientSFP([(epsilon, m), (epsilon_prime, m)], hash_families, cms_helper.generate_256_hash())

for i in range(0, N):
    word = np.random.choice(words)  # Sample randomly from our generated words
    dataset.append(word)  # Add the word to our dataset
    sfp_data.append(client_sfp.fragment(word))  # Client_SFP the word and add it to the sfp_data

freq_data = Counter(dataset)  # Generate frequency data on our original dataset
print("Data was privatised in: " + str(time.time()-start_time) + " seconds")
start_time = time.time()

# -------------------- Simulating the server-side process --------------------

server_sfp = ServerSFP([(epsilon, k, m), (epsilon_prime, k, m)], hash_families, threshold)
D, freq_oracle = server_sfp.generate_frequencies(sfp_data, alphabet)

print(D)

sfp_freq_data = HeavyHitterList(len(D))

for i in range(0, len(D)):
    sfp_freq_data.append((D[i], freq_oracle(D[i])))

print("Server Side SFP was calculated in: " + str(time.time()-start_time) + " seconds")
print("Plotting results...")
# -------------------- Plotting the data --------------------

fig, axs = plt.subplots(2)
ax1 = axs[0]
ax2 = axs[1]

color_palette = sns.cubehelix_palette(10, start=.5, rot=-.75, reverse=True)

# Plots the words and their frequencies in descending order
x1, y1 = zip(*freq_data.most_common())
sns.barplot(list(x1), list(y1), ax=ax1, palette=color_palette)
ax1.tick_params(rotation=45)
ax1.set_xlabel("Words")
ax1.set_ylabel("Word Count")
ax1.set_title("Words and their frequencies in the dataset")

x2, y2 = zip(*reversed(sfp_freq_data.get_data()))

# Generate colour palette for the the graph of sfp data
# We color bars of words that were discovered by sfp but were not in our original dataset as red
# We then maintain the coloring of the first graph for the words that were correctly discovered by sfp

palette = []
for data in list(x2):
    if data not in list(x1):
        palette.append("#e74c3c")
    else:
        palette.append(color_palette[(x1).index(data)])

# Plot the words discovered by sfp against estimated frequencies in descending order
sns.barplot(list(x2), list(y2), ax=ax2, palette=palette)
ax2.tick_params(rotation=45)
ax2.set_xlabel("Words Discovered")
ax2.set_ylabel("Estimated Word Count")
ax2.set_title("Discovered words and their estimated frequencies \n Using SFP(($\epsilon, \epsilon^\prime$) = {},{}, ($m,m^\prime$) = {},{}, ($k,k^\prime$)={},{})".format(epsilon, epsilon_prime,m,m,k,k))
fig.tight_layout()

print("Saving plot...")
plt.savefig("sfp.png")
plt.show()
print("Plot saved, simulation ended...")
