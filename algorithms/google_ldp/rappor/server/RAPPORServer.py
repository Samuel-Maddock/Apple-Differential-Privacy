from algorithms.google_ldp.rappor.client.RAPPORClient import RAPPORClient
from algorithms.google_ldp.rappor.client.rappor import Params, bit_string, get_bloom_bits
import pandas as pd
import subprocess
import csv, sys

class RAPPORServer:
    def __init__(self, num_bloombits, num_hashes, num_of_cohorts, probabilities):
        self.params = Params(num_bloombits, num_hashes, num_of_cohorts, probabilities)
        self.reports = []
        self.analysis_input_path = "./analysis_input/"
        self.analysis_output_path = "./analysis_output"

    def init_client_instance(self, cohort):
        return RAPPORClient(cohort, self.params)

    def add_report(self, report):
        self.reports.append(report)

    def clear_reports(self):
        self.reports = []

    def _write_params(self):
        with open('./analysis_input/_params.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            row1 = ["k", "h", "m", "p", "q", "f"]
            row2 = []

            for value in self.params.to_dict().values():
                row2.append(value)

            writer.writerow(row1)
            writer.writerow(row2)

    def _write_counts(self):
        with open('./analysis_input/_counts.csv', 'w', newline='') as f:
          writer = csv.writer(f)
          num_cohorts = self.params.num_cohorts
          num_bloombits = self.params.num_bloombits

          sums = [[0] * num_bloombits for _ in range(num_cohorts)]
          num_reports = [0] * num_cohorts

          for i, report in self.reports:
            (irr, cohort) = report
            cohort = int(cohort)
            num_reports[cohort] += 1

            if not len(irr) == num_bloombits:
              raise RuntimeError(
                  "Expected %d bits, got %r" % (num_bloombits, len(irr)))
            for i, c in enumerate(irr):
              bit_num = num_bloombits - i - 1  # e.g. char 0 = bit 15, char 15 = bit 0
              if c == '1':
                sums[cohort][bit_num] += 1
              else:
                if c != '0':
                  raise RuntimeError('Invalid IRR -- digits should be 0 or 1')

          for cohort in range(num_cohorts):
            # First column is the total number of reports in the cohort.
            row = [num_reports[cohort]] + sums[cohort]
            writer.writerow(row)

    def _write_map(self, items):
        with open('./analysis_input/_map.csv', 'w', newline='') as f:
            num_bloombits = self.params.num_bloombits
            num_hashes = self.params.num_hashes
            num_cohorts = self.params.num_cohorts
            writer = csv.writer(f)

            for item in items:
                row = [item]
                for cohort in range(num_cohorts):
                  bloom_bits = get_bloom_bits(bytes(item, "utf-8"), cohort, num_hashes, num_bloombits)
                  for bit_to_set in bloom_bits:
                    # bits are indexed from 1.  Add a fixed offset for each cohort.
                    # NOTE: This detail could be omitted from the map file format, and done
                    # in R.
                    row.append(cohort * num_bloombits + (bit_to_set + 1))
                writer.writerow(row)

    def get_freq(self, candidate_string):
        return self.generate_freq([candidate_string])

    def generate_freq_hist(self, candidate_strings):
        self._write_params()
        self._write_counts()
        self._write_map(candidate_strings)

        subprocess.call(["Rscript",  "compare_dist.R", self.analysis_input_path, self.analysis_input_path, self.analysis_output_path])

        freq_hist = pd.read_csv("./analysis_output/metrics.csv")
        return freq_hist