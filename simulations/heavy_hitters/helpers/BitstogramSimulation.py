from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from algorithms.bnst_ldp.Bitstogram.Bitstogram import Bitstogram


class BitstogramSimulation:
    def __init__(self, params):
        self.epsilon = params["epsilon"]
        self.R = params["R"]
        self.T = params["T"]
        self.word_length = params["max_string_length"]

    def run(self, data):
        h = cms_helper.generate_hash_funcs(self.R, self.T)
        heavy_hitters = Bitstogram(data, h, self.T, self.word_length, self.epsilon)

        return heavy_hitters.find_heavy_hitters()
