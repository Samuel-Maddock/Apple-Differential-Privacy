from algorithms.apple_ldp.cms.CMSHelper import cms_helper
from algorithms.bnst_ldp.Bitstogram.Bitstogram import Bitstogram


class BitstogramSimulation:
    def __init__(self, params):
        self.epsilon = params["epsilon"]
        self.R = params["R"]
        self.T = params["T"]
        self.binary_domain_size = params["binary_domain_size"]

    def run(self, data):
        print("Bitstogram is doing its thing...")
        h = cms_helper.generate_hash_funcs(self.R, self.T)
        heavy_hitters = Bitstogram(data, h, self.T, self.binary_domain_size, self.epsilon)
        print(heavy_hitters.find_heavy_hitters())

        return heavy_hitters.find_heavy_hitters()
