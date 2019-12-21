
from collections import Counter
from algorithms.bnst_ldp.TreeHistogram.ServerSide import runServerSideWordDiscovery
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
word_size = 6
word_sample_size = 10

# -------------------- Generating Test Data --------------------

# We generate all possible word_size character strings from our alphabet
# We then sample from this randomly to choose word_sample_size words
# We then use these words to sample our data from

print("TreeHist Word Count Simulation...")
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

data1 = ["abcaac"] * 10000
data2 = ["cccbba"] * 8000
data3 = ["aabbcc"] * 300

data = np.concatenate((data1,data2,data3))

print("Test data generated in: " + str(time.time()-start_time) + " seconds")
start_time = time.time()

# -------------------- Simulating the client-side process --------------------

dataset = []  # Dataset of words formed from our alphabet

for i in range(0, N):
    word = np.random.choice(words)  # Sample randomly from our generated words
    dataset.append(word)  # Add the word to our dataset


dataset = data

data = pd.DataFrame(list(dict(Counter(dataset)).items()), columns=["word", "trueFrequency"])

wordFreq = runServerSideWordDiscovery(data, "exp1", "results")

print(data)
print(wordFreq)