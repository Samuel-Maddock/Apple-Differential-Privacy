import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import os

from simulations.frequency_oracles.helpers.CMSSimulation import CMSSimulation
from simulations.frequency_oracles.helpers.PCSSimulation import PCSSimulation
from simulations.frequency_oracles.helpers.RAPPORSimulation import RAPPORSimulation
from simulations.frequency_oracles.helpers.HashtogramSimulation import HashtogramSimulation
from simulations.frequency_oracles.helpers.ExplicitHistSimulation import ExplicitHistSimulation

class NormalDistSimulation:
    def __init__(self, n, mu, sd):
        self.n = n
        self.mu = mu
        self.sd = sd
        self.data = np.random.normal(self.mu, self.sd, self.n).astype(int)  # Generate test data
        self.bins = np.arange(start=min(self.data), stop=max(self.data) + 1)
        self.experiment_plot_data = []

    def _run(self, experiment_list):
        for i in range(0, len(experiment_list)):
            experiment_name = experiment_list[i][0]
            params = experiment_list[i][1]

            experiment_output = self._run_experiment(experiment_name, params)
            self.experiment_plot_data.append((experiment_list[i], experiment_output))

    def _run_experiment(self, experiment_name, params):

        freq_oracles = {
            "cms": lambda parameters: CMSSimulation(parameters),
            "hcms": lambda parameters: CMSSimulation(parameters, is_hcms=True),
            "rappor": lambda parameters: RAPPORSimulation(parameters),
            "priv_count_sketch": lambda parameters: PCSSimulation(parameters),
            "explicit_hist": lambda parameters: ExplicitHistSimulation(parameters),
            "hashtogram": lambda parameters: HashtogramSimulation(parameters)
        }

        return freq_oracles.get(experiment_name, "error")(params).run(self.data, self.bins) # TODO: Provide error handling

    def _plot(self):
        bins = np.arange(start=min(self.data), stop=max(self.data) + 1)

        figsize = (len(self.experiment_plot_data)*5, len(self.experiment_plot_data)*5)

        fig, axs = plt.subplots(len(self.experiment_plot_data) + 2, figsize=figsize)
        colours = sns.color_palette("hls", len(self.experiment_plot_data) + 1) # Generate colours for each plot

        # Plotting a distplot of our integer data sampled from a normal dist
        sns.distplot(self.data, bins=bins, ax=axs[0], hist_kws={'ec': "black"}, color=colours[0])
        axs[0].set_title(
            "Integer data sampled from a Normal distribution \n $N=${}, sampled from $N({}, {})$".format(self.n,
                                                                                                         self.mu,
                                                                                                         self.sd * self.sd))
        for i, ldp_plot_data in enumerate(self.experiment_plot_data):
            experiment_name = ldp_plot_data[0][0]
            experiment_params = ldp_plot_data[0][1]
            experiment_data = ldp_plot_data[1]

            # Plotting a distplot of the data produced from the experiment
            sns.distplot(experiment_data, bins=bins, ax=axs[i + 1], color=colours[i+1], hist_kws={'ec': "black"})
            axs[i+1].set_title(
                "Differentially private " + experiment_name + " data produced from the normal sample \n Parameters: " + str(experiment_params))

            # Plotting the kde from above for comparison in the last axis
            sns.distplot(experiment_data, hist=False, bins=bins, ax=axs[len(axs)-1], color=colours[i+1])

        # Plot the original kde of the data in the last axis
        sns.distplot(self.data, bins=bins, hist=False, ax=axs[len(axs)-1], color=colours[0])

        fig.tight_layout()

        if not os.path.exists('plots'):
            os.mkdir('plots')

        filename = "plots/" + "experiment" + str(uuid.uuid4()) + ".png"

        plt.savefig(filename)
        plt.show()
        print("Plot Displayed...")

    def update_normal_params(self, n=None, mu=None, sd=None):
        self.n = self.n if n is None else n
        self.mu = self.mu if mu is None else mu
        self.sd = self.mu if mu is None else mu

        self.data = np.random.normal(self.mu, self.sd, self.n).astype(int)  # Re-generate test data
        self.bins = np.arange(start=min(self.data), stop=max(self.data) + 1)  # Re-generate bins for plots

        self.experiment_plot_data = []  # Clear experiment data

    def run_and_plot(self, experiment_list):
        self._run(experiment_list)
        self._plot()
