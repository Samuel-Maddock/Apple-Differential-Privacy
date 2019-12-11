# The core logic for private count sketch [Charikar-Chen-Farach-Colton 2004]
from .config import config
import numpy as np
import hashlib
from bitarray import bitarray
from bitstring import BitArray
from .DJWRandomizer import randomize
import math

class countSketch:
    sketchMatrix = np.zeros((config.l, config.w))

    @staticmethod
    def getSHA256HashArray(hashId, dataString):
        message = hashlib.sha256()

        message.update((str(hashId) + dataString).encode("utf8"))

        messageInBytes = message.digest()

        messageInBitArray = bitarray(endian='little')
        messageInBitArray.frombytes(messageInBytes)

        return messageInBitArray

    @staticmethod
    def setSketchElement(dataString):
        assert (isinstance(dataString, str) == True), 'Data should be a string'

        hashId = np.random.randint(0,config.l)
        messageInBitArray = countSketch.getSHA256HashArray(hashId, dataString)

        hLoc = BitArray(messageInBitArray[0: int(math.log(config.w, 2))]).uint
        gVal = 2 * messageInBitArray[int(math.log(config.w, 2))] - 1

        dataVec = np.zeros(config.w)
        dataVec[hLoc] = gVal

        privatizedVec = randomize(dataVec)

        countSketch.sketchMatrix[hashId]+= (privatizedVec * config.cEpsilon * config.l)


    @staticmethod
    def writeSketchToFile(sketchLocation):
        np.save(config.dataPath + sketchLocation, countSketch.sketchMatrix)

    @staticmethod
    def readSketch(sketchLocation):
        countSketch.sketchMatrix = np.load(config.dataPath + sketchLocation)

    @staticmethod
    def getFreqEstimate(dataString):
        assert (isinstance(dataString, str) == True), 'Data should be a string'

        weakFreqEstimates = np.zeros(config.l)
        for hashId in range(0, config.l):
            messageInBitArray = countSketch.getSHA256HashArray(hashId, dataString)

            hLoc = BitArray(messageInBitArray[0: int(math.log(config.w, 2))]).uint
            gVal = 2 * messageInBitArray[int(math.log(config.w, 2))] - 1
            weakFreqEstimates[hashId] = gVal * countSketch.sketchMatrix[hashId, hLoc]
        estimate = np.median(weakFreqEstimates)
        return estimate if estimate >0 else 0













