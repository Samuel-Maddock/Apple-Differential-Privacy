from algorithms.bnst_ldp.Bitstogram.Bitstogram import Bitstogram
from algorithms.apple_ldp.cms.CMSHelper import cms_helper
import numpy as np
import math

# Synthetic data
data1 = ["abcdee"] * 5000
data2 = ["helpme"] * 3000
data3 = ["whaton"] * 2000

data = np.concatenate((data1,data2,data3))

beta = 0.01
epsilon = 3
R = round(math.log(1/beta,2))
T = round((epsilon * 10000) / math.sqrt(R * 48))
print(R,T)
R = 1
T = 10

print(R,T)

h = cms_helper.generate_hash_funcs(R, T)
heavy_hitters = Bitstogram(data, h, T, 6, epsilon)

heavy_hitter_list = heavy_hitters.find_heavy_hitters()

print(heavy_hitter_list)