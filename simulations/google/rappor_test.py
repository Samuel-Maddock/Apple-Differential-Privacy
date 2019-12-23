from algorithms.google_ldp.rappor.server.RAPPORServer import RAPPORServer
import numpy as np

# ----------------------------- Parameters for the simulation: -------------------------

num_bloombits = 16
num_hashes = 2
num_of_cohorts = 64
prob_p = 0.50
prob_q = 0.75
prob_f = 0.50


# ----------------------------- Generating Test Data for the Simualtion: ----------------

data = np.random.normal(mu,sd,N).astype(int)



# ---------------------------------------------------------------------------------------

rappor_server = RAPPORServer(num_bloombits, num_hashes, num_of_cohorts, [prob_p, prob_q, prob_f])

for i in range(0, num_of_cohorts):
    rappor_client = rappor_server.init_client_instance(i)
    rappor_server.add_report(rappor_client.generate_report(data))


# ---------------------------------------------------------------------------------------
