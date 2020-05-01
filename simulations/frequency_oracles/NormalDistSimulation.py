import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import os
import pandas as pd

from simulations.frequency_oracles.helpers.FrequencyOracleSimulation import FrequencyOracleSimulation


class NormalDistSimulation(FrequencyOracleSimulation):
    def __init__(self, n, mu, sd):
        super().__init__()
        self.n = n
        self.mu = mu
        self.sd = sd
        self.data = np.random.normal(self.mu, self.sd, self.n).astype(int)  # Generate test data
        self.bins = np.arange(start=min(self.data), stop=max(self.data) + 1)
        self.experiment_plot_data = []

    def _plot(self):
        bins = np.arange(start=min(self.data), stop=max(self.data) + 1)

        figsize = (12, 20)

        fig, axs = plt.subplots(len(self.experiment_plot_data) + 1, figsize=figsize)
        colours = sns.color_palette("hls", len(self.experiment_plot_data) + 1)  # Generate colours for each plot

        # Plotting a distplot of our integer data sampled from a normal dist
        sns.distplot(self.data, bins=bins, ax=axs[0], hist_kws={'ec': "black"}, color=colours[0], label="Original")
        axs[0].set_title(
            "Integer data sampled from a Normal distribution \n $N=${}, sampled from $N({}, {})$".format(self.n,
                                                                                                         self.mu,
                                                                                                         self.sd * self.sd))

        row_list = []
        for i, ldp_plot_data in enumerate(self.experiment_plot_data):
            experiment_name = ldp_plot_data[0][0]
            experiment_params = ldp_plot_data[0][1]
            experiment_data = ldp_plot_data[1]
            experiment = ldp_plot_data[2]

            row = super().generate_stats(experiment_name, self.data, experiment_data, self.bins)
            row["client_time"] = ldp_plot_data[3][0]
            row["server_time"] = ldp_plot_data[3][1]
            row["total_time"] = ldp_plot_data[3][0] + ldp_plot_data[3][1]
            row_list.append(row)

            # Plotting a distplot of the data produced from the experiment
            sns.distplot(self.data, bins=bins, ax=axs[i + 1],  color=colours[0], hist_kws={'ec': "black"}, kde=False)
            sns.distplot(experiment_data, bins=bins, ax=axs[i + 1], color=colours[i + 1], hist_kws={'ec': "black"}, kde=False, label=experiment_name)

            axs[i + 1].set_title(
                experiment_name + "\n Parameters: " + str(
                    experiment_params))

            # # Plotting the kde from above for comparison in the last axis
            # sns.distplot(experiment_data, hist=False, bins=bins, ax=axs[len(axs) - 1], color=colours[i + 1])

        # # Plot the original kde of the data in the last axis
        # sns.distplot(self.data, bins=bins, hist=False, ax=axs[len(axs) - 1], color=colours[0])
        fig.legend()
        plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.2))

        fig.tight_layout()

        if not os.path.exists('plots'):
            os.mkdir('plots')

        name = str(uuid.uuid4())
        filename = "plots/" + "normal_exp" + name + ".png"

        plt.savefig(filename)

        stats = pd.DataFrame(row_list)
        pd.set_option('display.max_rows',0)
        pd.set_option('display.max_columns',500)
        pd.set_option('display.width',1000)
        pd.set_option('display.float_format', '{:.4f}'.format)

        print("\n", stats, "\n")
        stats.to_csv("plots/metrics/" + name + ".csv")
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
