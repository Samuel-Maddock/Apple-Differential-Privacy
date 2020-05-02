import sys
sys.path.append("..")

from simulations.frequency_oracles.NormalDistSimulation import NormalDistSimulation
from simulations.heavy_hitters.ExponentialDistSimulation import ExponentialDistSimulation
from simulations.heavy_hitters.NLTKSimulation import NLTKSimulation
from simulations.params import *
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from algorithms.apple_ldp.cms.server.ServerCMS import ServerCMS
import warnings
import math

# Parameters are stored in ./parameters.py
# Run one of these method's to see plots that correspond to the ones in the report

# warnings.filterwarnings("error", category=RuntimeWarning)

def cms_k_experiment(simulation, m=1, iters=100):
    experiment_list = []
    for i in range(0, iters):
        cms_copy = cms.copy()
        cms_copy["k"] = m + (i * m)
        cms_copy["m"] = 50
        experiment_list.append(("cms", cms_copy))

    simulation.run_and_plot(experiment_list)


def threshold_sfp_experiment(simulation, T=10, iters=20):
    experiment_list = []
    for i in range(0, iters):
        sfp_copy = sfp.copy()
        sfp_copy["threshold"] = T + (i * T)
        experiment_list.append(("sfp t=" + str(sfp_copy["threshold"]), sfp_copy))

    simulation.run_and_plot(experiment_list)


def threshold_experiment(simulation, T=10, iters=20):
    experiment_list = []
    for i in range(0, iters):
        tree_copy = treehistogram.copy()
        tree_copy["threshold"] = T + (i * T)
        experiment_list.append(("treehistogram t=" + str(tree_copy["threshold"]), tree_copy))

    simulation.run_and_plot(experiment_list)


def normal_dist_experiment():
    normal_simulation = NormalDistSimulation(N, mu, sd)
    normal_simulation.run_and_plot([("cms", cms), ("hcms", cms), ("priv_count_sketch", priv_count_sketch),
                                    ("priv_count_sketch_median", priv_count_sketch), ("explicit_hist", explicit_hist),
                                    ("hashtogram", hashtogram), ("hashtogram_median", hashtogram), ("rappor", rappor)])


def sfp_with_diff_freq_oracles():
    exponential_simulation = ExponentialDistSimulation(N, p, alphabet, word_length, word_sample_size)
    exponential_simulation.run_and_plot([("sfp", sfp_3), ("sfp", sfp), ("sfp", sfp_1)])


def treehist_with_diff_freq_oracles():
    exponential_simulation = ExponentialDistSimulation(N, p, alphabet, word_length, word_sample_size)
    exponential_simulation.run_and_plot(
        [("treehistogram", treehist_3), ("treehistogram", treehistogram), ("treehistogram", treehist_1)])


def sfp_with_diff_params():
    exponential_simulation = ExponentialDistSimulation(N, p, alphabet, word_length, word_sample_size)
    exponential_simulation.run_and_plot(
        [("sfp", sfp2), ("sfp", sfp3), ("sfp", sfp1), ("sfp", sfp4), ("sfp", sfp), ("sfp", sfp5)])


def treehist_with_diff_params():
    exponential_simulation = ExponentialDistSimulation(N, p, alphabet, word_length, word_sample_size)
    exponential_simulation.run_and_plot(
        [("treehistogram", treehist1), ("treehistogram", treehist2), ("treehistogram", treehist3),
         ("treehistogram", treehist4), ("treehistogram", treehist5), ("treehistogram", treehist6)])


def pcs_with_diff_epsilon():
    normal_simulation = NormalDistSimulation(N, mu, sd)
    normal_simulation.run_and_plot([("priv_count_sketch e=3", priv_count_sketch), ("priv_count_sketch e=1.5", pcs2),
                                    ("priv_count_sketch e=1", pcs3), ("priv_count_sketch e=0.5", pcs4)])


# Run one of the above methods to see experiment results, plots will be generated and saved under a folder in frequency_oracles/plots
# If using an IDE like PyCharm plots should also display in the scientific view
# Experiment Metrics will also be output to the console and in a file under frequency_oracle/plots/metrics

normal_dist_experiment()
