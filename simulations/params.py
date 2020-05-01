from algorithms.apple_ldp.cms.CMSHelper import cms_helper
import math

# #-------------------- Parameters for simulation --------------------

# --------- General Parameters -----------
N = 10000
epsilon = 3  # 1, 0.1

# --------- Normal Dist Experiment -----------
mu = 10
sd = 3

# --------- Exponential Dist Experiment -----------
p = 0.3
alphabet = set(list("abc"))
word_length = 6
word_sample_size = 10

# --------- CMS/HCMS Parameters -----------
m = 2048
k = 1024

# --------- SFP -----------
epsilon_prime = 1
threshold = 100

# --------- RAPPOR -----------
num_bloombits = 128  # Max size is 256 bits
num_hashes = 2  # Recommended to use 2 hashes
num_of_cohorts = 32  # Max cohorts is 64

# Guarantees slightly over epsilon = 1 for privacy
# prob_p = 0.7
# prob_q = 0.4
# prob_f = 0

# prob_p = 0.35
# prob_q = 0.7
# prob_f = 0

prob_p = 0.5
prob_q = 0.75
prob_f = 0

# prob_p = 0.5
# prob_q = 0.53
# prob_f = 0

# --------- Hashtogram -----------
R = 100
T = 100

m = 2048
k = 1024  # We use k = k_prime and m = m_prime for our simulation


# PrivCountSketch Parameters
l = 250
numBits = int(math.floor(math.log(N, 2)) + 1)
w = 2 ** numBits

cms = {"m": m, "k": k, "epsilon": epsilon}
priv_count_sketch = {"l": l, "w": w, "epsilon": epsilon}

explicit_hist = {"epsilon": epsilon}

hashtogram = {"epsilon": epsilon, "R": R, "T": T}

rappor = {
    "num_bloombits": num_bloombits,
    "num_hashes": num_hashes,
    "num_of_cohorts": num_of_cohorts,
    "prob_p": prob_p,
    "prob_q": prob_q,
    "prob_f": prob_f
}

pcs2 = priv_count_sketch.copy()
pcs2["epsilon"] = 1.5

pcs3 = priv_count_sketch.copy()
pcs3["epsilon"] = 1

pcs4 = priv_count_sketch.copy()
pcs4["epsilon"] = 0.5

pcs5 = priv_count_sketch.copy()
pcs5["epsilon"] = 0.1

# ------------------ Heavy Hitter Parameters -----------------------

bitstogram = {
    "epsilon": epsilon,
    "R": 5,
    "T": 2000,
    "max_string_length": word_length
}

succincthist = {
    "epsilon": epsilon,
    "max_string_length": word_length,
    "T": 350,
}

d = word_length * 8
logd = d

numBits = int(math.floor(math.log(math.sqrt(N), 2)) + 1)
w = 2 ** numBits  # Sketch size
w = 128
assert (int(math.log(w, 2)) <= 254), 'Sketch size (w) too large'

l = 250  # Number of hash function pairs (f,g)

num_n_grams = 3  # Number of N-grams
gram_length = 2  # Gram length
threshold = 3 * int(math.sqrt(N))  # Threshold for discoverability

hash_funcs = cms_helper.generate_hash_funcs(T, R)
params = {"epsilon": epsilon, "T": T, "hash_family": hash_funcs}

sfp = {
    "m": m,
    "k": k,
    "epsilon": 2,
    "m_prime": m,
    "k_prime": k,
    "epsilon_prime": 6,
    "threshold": 50,
    "alphabet": alphabet,
    "fragment_length": 2,
    "max_string_length": 6
}

hash_family = cms_helper.generate_hash_funcs(k, m)
cms_params = {"epsilon": epsilon,
              "k": k,
              "m": m,
              "hash_funcs": hash_family
              }

sfp1 = sfp.copy()
sfp1["freq_oracle"] = "priv_count_sketch"
sfp1["freq_oracle_params"] = priv_count_sketch

sfp2 = sfp.copy()
sfp2["freq_oracle"] = "hashtogram"
sfp2["freq_oracle_params"] = params

sfp3 = sfp2.copy()
sfp3["freq_oracle"] = "hashtogram_median"

sfp4 = sfp1.copy()
sfp4["freq_oracle"] = "priv_count_sketch_median"

sfp5 = sfp.copy()
sfp5["freq_oracle"] = "hcms"
sfp5["freq_oracle_params"] = cms_params

sfp_1 = sfp.copy()
sfp_1["fragment_length"] = 1

sfp_3 = sfp.copy()
sfp_3["fragment_length"] = 3


treehistogram = {
    "epsilon": epsilon,
    "l": l,
    "w": 2048,
    "max_string_length": word_length,
    "gram_length": gram_length,
    "threshold": 50,
    "alphabet": alphabet
}


treehist1 = treehistogram.copy()
treehist1["freq_oracle"] = "hashtogram"
treehist1["freq_oracle_params"] = params

treehist2 = treehistogram.copy()
treehist2["freq_oracle"] = "hashtogram_median"
treehist2["freq_oracle_params"] = params

treehist3 = treehistogram.copy()
treehist3["freq_oracle"] = "priv_count_sketch"
treehist3["freq_oracle_params"] = priv_count_sketch

treehist4 = treehistogram.copy()
treehist4["freq_oracle"] = "priv_count_sketch_median"
treehist4["freq_oracle_params"] = priv_count_sketch

treehist5 = treehistogram.copy()
treehist5["freq_oracle"] = "cms"
treehist5["freq_oracle_params"] = cms_params

treehist6 = treehistogram.copy()
treehist6["freq_oracle"] = "hcms"
treehist6["freq_oracle_params"] = cms_params

treehist_1 = treehistogram.copy()
treehist_1["gram_length"] = 1

treehist_3 = treehistogram.copy()
treehist_3["gram_length"] = 3