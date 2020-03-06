import nltk
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import os
import itertools

from nltk.corpus import words
from nltk.corpus import brown
from nltk.corpus import nps_chat
from nltk.corpus import dependency_treebank
from collections import Counter

from simulations.heavy_hitters.helpers.HeavyHitterSimulation import HeavyHitterSimulation


class NLTKSimulation(HeavyHitterSimulation):
    def __init__(self, sample_size):
        super().__init__()
        self.experiment_plot_data = []
        self.alphabet = []
        self.max_string_length = 0
        self.sample_size = sample_size
        self.data = self._generate_dataset()

    def _generate_dataset(self):
        word = nltk.FreqDist(dependency_treebank.words())

        freq_dataset = word.most_common(30)
        freq_dataset = freq_dataset[29:10:-1]

        dataset = []
        alphabet = set()
        max_string_length = 0

        for pair in freq_dataset:
            dataset += [pair[0]] * pair[1]
            if len(pair[0]) > max_string_length:
                max_string_length = len(pair[0])

            for char in pair[0]:
                alphabet.add(char)

        for element in dataset:
            for char in element:
                alphabet.add(char)

        self.alphabet = alphabet

        if max_string_length % 2 != 0:
            max_string_length = max_string_length + 1

        self.max_string_length = max_string_length
        print("Length of dataset is", len(dataset))
        print(alphabet)
        return dataset

    def _run_experiment(self, experiment_name, params):
        params["alphabet"] = self.alphabet
        params["max_string_length"] = self.max_string_length

        super()._run_experiment(experiment_name, params)

    def __plot(self):
        freq_data = Counter(self.data)
        print("Plotting results...")

        figsize = (len(self.experiment_plot_data) * 10, len(self.experiment_plot_data) * 10)
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

        for i, plot_data in enumerate(self.experiment_plot_data):
            experiment_name = plot_data[0][0]
            experiment_params = plot_data[0][1]
            heavy_hitter_data = plot_data[1]

            ax = axs[i + 1]

            if len(heavy_hitter_data) == 0:
                heavy_hitter_data.add(("empty", 0))

            x, y = zip(*reversed(heavy_hitter_data))
            palette = self._generate_palette(color_palette, x1, x)

            # Plot the words discovered by the heavy hitter against estimated frequencies in descending order
            sns.barplot(list(x), list(y), ax=ax, palette=palette)
            ax.tick_params(rotation=45)
            ax.set_xlabel("Words Discovered")
            ax.set_ylabel("Estimated Word Count")

            ax.set_title(
                "Discovered words and their estimated frequencies \n Experiment: " + experiment_name)
            # + "\n Parameters: " + str(experiment_params) )

        fig.tight_layout()

        if not os.path.exists('plots'):
            os.mkdir('plots')

        filename = "plots/" + "nltk_exp" + str(uuid.uuid4()) + ".png"
        plt.savefig(filename)
        plt.show()
        print("Plot saved, simulation ended...")

    def run_and_plot(self, experiment_list):
        self._run(experiment_list)
        self.__plot()
