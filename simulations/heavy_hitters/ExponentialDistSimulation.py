import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import os
import itertools
from collections import Counter
from simulations.heavy_hitters.helpers.SFPSimulation import SFPSimulation
from simulations.heavy_hitters.helpers.TreehistogramSimulation import TreeHistogramSimulation
from simulations.heavy_hitters.helpers.SuccinctHistSimulation import SuccinctHistSimulation
from simulations.heavy_hitters.helpers.BitstogramSimulation import BitstogramSimulation

class ExponentialDistSimulation:
    def __init__(self, n, p, alphabet, word_length, word_sample_size):
        self.n = n
        self.p = p
        self.alphabet = alphabet
        self.word_length = word_length
        self.word_sample_size = word_sample_size
        self.experiment_plot_data = []
        self.data = self._generate_dataset()

    def _generate_dataset(self):
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

    def _run(self, experiment_list):
        for i in range(0, len(experiment_list)):
            experiment_name = experiment_list[i][0]
            params = experiment_list[i][1]

            experiment_output = self._run_experiment(experiment_name, params)
            self.experiment_plot_data.append((experiment_list[i], experiment_output))

    def _run_experiment(self, experiment_name, params):
        heavy_hitters = {
            "sfp": lambda parameters: SFPSimulation(parameters),
            "treehistogram": lambda parameters: TreeHistogramSimulation(parameters),
            "succincthist": lambda parameters: SuccinctHistSimulation(parameters),
            "bitstogram": lambda parameters: BitstogramSimulation(parameters)
        }

        return heavy_hitters.get(experiment_name, "error")(params).run(self.data)  # TODO: Provide error handling

    def  _generate_palette(self, color_palette, x1, x2):
        # Generate colour palette for a graph of heavy hitter data
        # We color bars of words that were discovered by the algo but were not in our original dataset as red
            # We maintain the original coloring of the words that were correctly discovered

        palette = []
        for data in list(x2):
            if data not in list(x1):
                palette.append("#e74c3c")
            else:
                palette.append(color_palette[x1.index(data)])
        return palette

    def _plot(self):
        freq_data = Counter(self.data)
        print("Plotting results...")

        fig, axs = plt.subplots(len(self.experiment_plot_data)+1, figsize=(8, 8))
        ax1 = axs[0]

        # Plots the words and their frequencies in descending order
        x1, y1 = zip(*freq_data.most_common())
        color_palette = sns.cubehelix_palette(len(x1), start=.5, rot=-.75, reverse=True)
        sns.barplot(list(x1), list(y1), ax=ax1, palette=color_palette)
        ax1.tick_params(rotation=45)
        ax1.set_xlabel("Words")
        ax1.set_ylabel("Word Count")
        ax1.set_title("Words and their frequencies in the dataset")

        for i, plot_data in enumerate(self.experiment_plot_data):
            experiment_name = plot_data[0][0]
            params = plot_data[0][1]
            heavy_hitter_data = plot_data[1]

            ax = axs[i+1]
            x, y = zip(*reversed(heavy_hitter_data))
            palette = self._generate_palette(color_palette, x1, x)

            # Plot the words discovered by the heavy hitter against estimated frequencies in descending order
            sns.barplot(list(x), list(y), ax=ax, palette=palette)
            ax.tick_params(rotation=45)
            ax.set_xlabel("Words Discovered")
            ax.set_ylabel("Estimated Word Count")
            ax.set_title(
                "Discovered words and their estimated frequencies \n Experiment: " + experiment_name)

        fig.tight_layout()

        if not os.path.exists('plots'):
            os.mkdir('plots')

        filename = "plots/" + "exponential_exp" + str(uuid.uuid4()) + ".png"
        plt.savefig(filename)
        plt.show()
        print("Plot saved, simulation ended...")

    def run_and_plot(self, experiment_list):
        self._run(experiment_list)
        self._plot()
