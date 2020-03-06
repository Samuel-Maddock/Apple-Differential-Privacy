from simulations.heavy_hitters.helpers.SFPSimulation import SFPSimulation
from simulations.heavy_hitters.helpers.TreehistogramSimulation import TreeHistogramSimulation
from simulations.heavy_hitters.helpers.SuccinctHistSimulation import SuccinctHistSimulation
from simulations.heavy_hitters.helpers.BitstogramSimulation import BitstogramSimulation

from collections import OrderedDict

class HeavyHitterSimulation:
    def __init__(self):
        self.data = []
        self.experiment_plot_data = []
        pass

    def _run(self, experiment_list):
        for i in range(0, len(experiment_list)):
            experiment_name = experiment_list[i][0]
            params = experiment_list[i][1]
            experiment_freq_oracle = "" if params.get("freq_oracle", None) is None else params.get("freq_oracle")

            print("Running experiment", i + 1, ":", experiment_name, "with", experiment_freq_oracle, "\nParams: \n %.300s...\n" % params.__str__())

            experiment, experiment_output = self._run_experiment(experiment_name, params)
            self.experiment_plot_data.append((experiment_list[i], experiment_output, experiment))

    def _run_experiment(self, experiment_name, params):
        heavy_hitters = {
            "sfp": lambda parameters: SFPSimulation(parameters),
            "treehistogram": lambda parameters: TreeHistogramSimulation(parameters),
            "succincthist": lambda parameters: SuccinctHistSimulation(parameters),
            "bitstogram": lambda parameters: BitstogramSimulation(parameters)
        }

        if experiment_name not in heavy_hitters.keys():
            assert "experiment name must be one of: ", heavy_hitters.keys()

        experiment = heavy_hitters.get(experiment_name)(params)

        return experiment, experiment.run(self.data)

    def _generate_palette(self, color_palette, x1, x2):
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

    def generate_metrics(self, experiment_name, original_data, heavy_hitter_data, sample_size):
        row = OrderedDict()

        heavy_hitter_data = dict(heavy_hitter_data)

        tp = 0
        avg_freq = 0
        for word in heavy_hitter_data.keys():
            if word in original_data.keys():
                tp += 1
            else:
                avg_freq += heavy_hitter_data[word]
        fp = len(heavy_hitter_data.keys()) - tp

        row["freq_oracle"] = experiment_name
        row["recall"] = tp / len(original_data.keys())
        row["precision"] = tp / len(heavy_hitter_data.keys())
        row["false_positives"] = fp
        row["average_freq_of_fp"] = avg_freq/fp if fp != 0 else "NA"

        return row
