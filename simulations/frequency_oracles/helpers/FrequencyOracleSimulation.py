import numpy as np

from algorithms.bnst_ldp.Bitstogram.ExplicitHist import ExplicitHist
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from collections import Counter, OrderedDict

from simulations.frequency_oracles.helpers.CMSSimulation import CMSSimulation
from simulations.frequency_oracles.helpers.PCSSimulation import PCSSimulation
from simulations.frequency_oracles.helpers.RAPPORSimulation import RAPPORSimulation
from simulations.frequency_oracles.helpers.HashtogramSimulation import HashtogramSimulation
from simulations.frequency_oracles.helpers.ExplicitHistSimulation import ExplicitHistSimulation

class FrequencyOracleSimulation:

    def __init__(self):
        self.name = "Frequency Oracle"
        self.experiment_plot_data = []
        self.data = []
        self.bins = []

    def run(self, data, domain):
        assert "Must implement"

    def _run(self, experiment_list):
        for i in range(0, len(experiment_list)):
            experiment_name = experiment_list[i][0]
            params = experiment_list[i][1]

            print("Running experiment", i + 1, ":", experiment_name, "with params: \n", params.__str__(), "\n")

            experiment, experiment_output = self._run_experiment(experiment_name, params)
            self.experiment_plot_data.append((experiment_list[i], experiment_output[0], experiment, experiment_output[1:3]))

    def _run_experiment(self, experiment_name, params):

        freq_oracles = {
            "cms": lambda parameters: CMSSimulation(parameters),
            "hcms": lambda parameters: CMSSimulation(parameters, is_hcms=True),
            "rappor": lambda parameters: RAPPORSimulation(parameters),
            "priv_count_sketch": lambda parameters: PCSSimulation(parameters),
            "priv_count_sketch_median": lambda parameters: PCSSimulation(parameters, use_median=True),
            "explicit_hist": lambda parameters: ExplicitHistSimulation(parameters),
            "hashtogram": lambda parameters: HashtogramSimulation(parameters),
            "hashtogram_median": lambda parameters: HashtogramSimulation(parameters, use_median=True)
        }

        if experiment_name not in freq_oracles.keys():
            assert "experiment name must be one of: ", freq_oracles.keys()

        experiment = freq_oracles.get(experiment_name)(params)

        return experiment, experiment.run(self.data, self.bins)

    def __calculate_error(self, data, ldp_data, domain):
        original_freq_data = dict(Counter(data.tolist()))
        ldp_freq_data = dict(Counter(ldp_data.tolist()))

        mse = 0
        max_error = 0
        total_error = 0
        max_item = ""

        for item in domain:
            error = abs(ldp_freq_data.get(item, 0) - original_freq_data.get(item, 0))
            if max_error < error:
                max_error = error
                max_item = item
            total_error += error
            mse += error**2

        avg_error = total_error / len(domain)
        mse = mse / len(domain)

        return max_error, max_item, avg_error, mse

    def generate_stats(self, experiment_name, data, ldp_data, domain):
        row = OrderedDict()
        max_error, max_item, avg_error, mse = self.__calculate_error(data, ldp_data, domain)

        row["freq_oracle"] = experiment_name
        row["mse"] = mse
        row["average_error"] = avg_error
        row["max_error"] = max_error
        row["max_item"] = max_item

        return row

