from algorithms.google_ldp.rappor.server.RAPPORServer import RAPPORServer
from collections import Counter

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------- Parameters for the simulation: -------------------------

num_bloombits = 128 # Max size is 256 bits
num_hashes = 2 # Recommended to use 2 hashes
num_of_cohorts =  32 # Max cohorts is 64

# Guarantees slightly over epsilon = 1 for privacy
prob_p = 0.5
prob_q = 0.75
prob_f = 0

n = 100000

# Normal Dist Parameters
mu = 50
sd = 10


# ----------------------------- Generating Test Data for the Simulation: ----------------

data = np.random.normal(mu,sd,n).astype(int)
bins = np.arange(start=min(data), stop = max(data) + 1)

print(dict(Counter(data)))
fig, axs = plt.subplots(2)

# ---------------------------------------------------------------------------------------

rappor_server = RAPPORServer(num_bloombits, num_hashes, num_of_cohorts, [prob_p, prob_q, prob_f])

for i in range(0, n):
    rappor_client = rappor_server.init_client_instance(np.random.randint(0, num_of_cohorts-1))
    rappor_server.add_report(rappor_client.generate_report(str(data[i])))

print("\n")

hist = rappor_server.generate_freq_hist(list(map(lambda x: str(x), bins)))
print(hist)

ldp_data = np.zeros(len(bins))
for row in hist.values.tolist():
    ldp_data = np.append(ldp_data, [int(row[0])]*int(row[1]))

print(ldp_data)

# -------------------- Plotting the data --------------------
print("Plotting data...")

# Plotting a distplot of our integer data sampled from a normal dist
sns.distplot(data, bins=bins, ax=axs[0], hist_kws={'ec': "black"})
axs[0].set_title("RAPPOR")

# Plotting a distplot of the data produced from the CMS algorithm
sns.distplot(ldp_data, bins=bins, ax=axs[0], color='r', hist_kws={'ec': "black"})
axs[1].set_title("RAPPOR")

# Plotting both kde's from above for comparison
sns.distplot(ldp_data, hist=False, bins=bins, ax=axs[1], color='r')
sns.distplot(data, bins=bins, hist=False, ax=axs[1])

fig.tight_layout()
plt.savefig("rappor.png")
plt.show()
print("Plot Displayed !")
