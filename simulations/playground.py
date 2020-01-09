from simulations.frequency_oracles.NormalDistSimulation import NormalDistSimulation
import math

# -------------------- Parameters for simulation --------------------

# Normal Dist Parameters
N = 10000
mu = 10
sd = 3

# CMS/HCMS Parameters
m = 2048
k = 1024
epsilon = 3

# PrivCountSketch Parameters
l = 250
numBits = int(math.floor(math.log(N, 2)) + 1)
w = 2**numBits

# RAPPOR Parameters
num_bloombits = 128  # Max size is 256 bits
num_hashes = 2  # Recommended to use 2 hashes
num_of_cohorts = 32  # Max cohorts is 64

# Guarantees slightly over epsilon = 1 for privacy
prob_p = 0.5
prob_q = 0.75
prob_f = 0

# Hashtogram Parameters
R = 100
T =  100

# -------------------- Simulation Code --------------------

normal_simulation = NormalDistSimulation(N, mu, sd)

cms = {"m": m, "k": k, "epsilon": epsilon}
priv_count_sketch = {"l": l, "w": w, "epsilon": epsilon}
explicit_hist = {"epsilon": epsilon}
hashtogram = {"epsilon": epsilon, "R": R, "T": R}

rappor = {
    "num_bloombits": num_bloombits,
    "num_hashes": num_hashes,
    "num_of_cohorts": num_of_cohorts,
    "prob_p": prob_p,
    "prob_q": prob_q,
    "prob_f": prob_f
}

normal_simulation.run_and_plot([("cms", cms), ("hcms", cms), ("priv_count_sketch", priv_count_sketch), ("explicit_hist", explicit_hist), ("hashtogram", hashtogram), ("rappor", rappor)])
