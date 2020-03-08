import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import os
import itertools
import pandas as pd
from collections import Counter

from simulations.heavy_hitters.helpers.HeavyHitterSimulation import HeavyHitterSimulation


class ExponentialDistSimulation(HeavyHitterSimulation):
    def __init__(self, n, p, alphabet, word_length, word_sample_size):
        super().__init__()
        self.n = n
        self.p = p
        self.alphabet = alphabet
        self.word_length = word_length
        self.word_sample_size = word_sample_size
        self.experiment_plot_data = []
        self.data = self.__generate_dataset()

    def __generate_dataset(self):
        dataset = []
        alphabet_list = []

        for i in range(0, self.word_length):
            alphabet_list.append(self.alphabet)

        # Form all possible strings of length word_size from our given alphabet
        strings = list(set(map(lambda x: str().join(x), itertools.product(*alphabet_list))))

        def generate_words(n):
            words = set()
            for i in range(0, n):
                words.add(np.random.choice(strings))
            return list(words)

        words = generate_words(self.word_sample_size)

        geometric = Counter(np.random.geometric(p=self.p, size=self.n))

        for i, word in enumerate(words):
            frequency = geometric.get(i + 1)

            for j in range(0, frequency):
                dataset.append(word)  # Add the word to our dataset

        return dataset

    def __plot(self):
        freq_data = Counter(self.data)
        print("Plotting results...")

        figsize = (len(self.experiment_plot_data) * 3, len(self.experiment_plot_data) * 5)
        fig, axs = plt.subplots(len(self.experiment_plot_data) + 1, figsize=figsize)
        ax1 = axs[0]

        # Plots the words and their frequencies in descending order
        x1, y1 = zip(*freq_data.most_common())
        color_palette = sns.cubehelix_palette(len(x1), start=.5, rot=-.75, reverse=True)
        sns.barplot(list(x1), list(y1), ax=ax1, palette=color_palette)
        ax1.tick_params(rotation=45)
        ax1.set_xlabel("Words")
        ax1.set_ylabel("Word Count")
        ax1.set_title("Words and their frequencies in the dataset")

        row_list = []
        for i, plot_data in enumerate(self.experiment_plot_data):
            experiment_name = plot_data[0][0]
            experiment_params = plot_data[0][1]
            heavy_hitter_data = plot_data[1]
            experiment = plot_data[2]

            ax = axs[i + 1]

            if len(heavy_hitter_data) == 0:
                heavy_hitter_data.add(("empty", 0))

            # Generate metrics for this experiment
            experiment_freq_oracle = "" if experiment_params.get("freq_oracle", None) is None else " with " + experiment_params.get("freq_oracle")

            row = super().generate_metrics(experiment_name+experiment_freq_oracle, freq_data, heavy_hitter_data, self.word_sample_size)
            row["client_time"] = plot_data[3][0]
            row["server_time"] = plot_data[3][1]
            row["total_time"] = plot_data[3][0] + plot_data[3][1]
            row_list.append(row)

            x, y = zip(*reversed(heavy_hitter_data))
            palette = self._generate_palette(color_palette, x1, x)

            # Plot the words discovered by the heavy hitter against estimated frequencies in descending order
            sns.barplot(list(x), list(y), ax=ax, palette=palette)
            ax.tick_params(rotation=45)
            ax.set_xlabel("Words Discovered")
            ax.set_ylabel("Estimated Word Count")

            if experiment_params.get("freq_oracle") is not None:
                experiment_name = experiment_name + " with " + experiment_params["freq_oracle"]

            ax.set_title(
                "Discovered words and their estimated frequencies \n Experiment: " + experiment_name)
            # + "\n Parameters: " + str(experiment_params) )

        pd.set_option('display.max_columns',500)
        pd.set_option('display.width',1000)
        pd.set_option('display.max_rows',0)
        pd.set_option('display.float_format', '{:.4f}'.format)
        metrics = pd.DataFrame(row_list)
        print("\n", metrics, "\n")

        fig.tight_layout()

        if not os.path.exists('plots'):
            os.mkdir('plots')

        filename = "plots/" + "exponential_exp" + str(uuid.uuid4()) + ".png"
        plt.savefig(filename)
        plt.show()
        print("Plot saved, simulation ended...")

    def run_and_plot(self, experiment_list):
        self._run(experiment_list)
        self.__plot()
