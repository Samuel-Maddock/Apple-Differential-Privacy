from algorithms.google_ldp.rappor.server.RAPPORServer import RAPPORServer
from collections import Counter

import numpy as np

# ----------------------------- Parameters for the simulation: -------------------------

num_bloombits = 16
num_hashes = 2
num_of_cohorts = 64
prob_p = 0.50
prob_q = 0.75
prob_f = 0

n = 1000000
zipf_param = 1.3

# ----------------------------- Generating Test Data for the Simulation: ----------------

data = np.random.zipf(zipf_param, n).astype(int)

# ---------------------------------------------------------------------------------------

rappor_server = RAPPORServer(num_bloombits, num_hashes, num_of_cohorts, [prob_p, prob_q, prob_f])

for i in range(0, n):
    rappor_client = rappor_server.init_client_instance(np.random.randint(0, num_of_cohorts-1))
    rappor_server.add_report(rappor_client.generate_report(str(data[i])))

print("\n")
print(Counter(data))

hist = rappor_server.generate_freq_hist(["1", "3"])
print(hist)

# ---------------------------------------------------------------------------------------
