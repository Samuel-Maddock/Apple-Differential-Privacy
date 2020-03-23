# Duchi-Jordan-Wainwright 2013, Bassily-Smith-2015 randomizer
import numpy as np
import math

def randomize(bitVec, epsilon):
    unsignedBits = np.abs(bitVec)
    assert (np.sum(unsignedBits) == 1.0), 'Incorrect number of bits set in the data vector'
    indexOfData = np.where(unsignedBits == 1)[0][0]

    unBiasedPMBits = 2 * np.random.binomial(1, 0.5, len(bitVec)) - 1
    unBiasedPMBits[indexOfData] = 0
    privatizedBitVec = unBiasedPMBits + bitVec

    bias = math.exp(epsilon) / (1 + math.exp(epsilon))
    privatizedBitVec[indexOfData] *= (2 * np.random.binomial(1,bias) - 1)
    return privatizedBitVec