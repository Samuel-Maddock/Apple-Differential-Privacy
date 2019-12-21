# Add the configuration parameters for the framework
import math
import numpy as np

class config:
    @staticmethod
    def reinitializeParameters():
        config.epsilon = 2.0  # Privacy parameter, to be set globally
        config.cEpsilon = (math.exp(config.epsilon) + 1) / (math.exp(config.epsilon) - 1)  # Scaling for de-biasing

        config.p = 10000  # Domain size
        config.n = 100000  # Number of data samples, needed only for simulation

        config.w = config.nearestPowerOfTwoCeil(math.sqrt(config.n))  # Sketch size
        assert (int(math.log(config.w, 2)) <= 254), 'Sketch size (w) too large'

        config.l = 250  # Number of hash function pairs (f,g)

        config.numNgrams = 3  # Number of N-grams
        config.gramLength = 2  # Gram length
        config.emptyChar = '?'  # Character to fill the word with if words are smaller
        config.threshold = 15.0 * int(math.sqrt(config.n))  # Threshold for discoverability

    @staticmethod
    def chooseRandomNGramPrefix(word,N):
        assert len(word) % N ==0, 'Word = ' + word + ' is not of correct length'
        randomStartIndex = np.random.randint(0,len(word)/N) * N
        randomPrefixWord = word[0:randomStartIndex+N] + config.emptyChar * (config.gramLength * config.numNgrams - len(word[0:randomStartIndex+N]))
        return randomPrefixWord

    # Generate a an array of N-grams
    @staticmethod
    def checkArrayCounterMaxReached(arrayOfCounters):
        if arrayOfCounters[0] == 3:
            return True
        return False

    @staticmethod
    def incrementArray(arrayOfCounters):
        arrayOfCounters[-1] += 1
        for i in range(len(arrayOfCounters) - 1, 0, -1):
            if arrayOfCounters[i] == 3:
                arrayOfCounters[i] = 0
                arrayOfCounters[i - 1] += 1

    @staticmethod
    def genEnglishNgrams(N):
        gramDict = [''] * (int(math.pow(3, N)))
        counter = 0
        wordLength = config.gramLength
        arrayOfCounters = [0] * wordLength
        while (config.checkArrayCounterMaxReached(arrayOfCounters) == False):
            for x in arrayOfCounters:
                gramDict[counter] += chr(97 + x)
            counter += 1
            config.incrementArray(arrayOfCounters)
        return gramDict

    # Get the nearest power of two for a given number
    @staticmethod
    def nearestPowerOfTwoCeil(num):
        numBits = int(math.floor(math.log(num, 2)) + 1)
        return 2**numBits

    epsilon = 1.0    # Privacy parameter, to be set globally
    cEpsilon = (math.exp(epsilon) + 1)/(math.exp(epsilon) - 1)  # Scaling for de-biasing

    p = 10000000     # Domain size
    n = 10000      # Number of data samples, needed only for simulation

    w = nearestPowerOfTwoCeil.__func__(math.sqrt(n)) # Sketch size
    assert (int(math.log(w, 2)) <= 254), 'Sketch size (w) too large'

    l = 250          # Number of hash function pairs (f,g)

    numNgrams = 3
    gramLength = 2  # Gram length
    emptyChar = '?'  # Character to fill the word with if words are smaller
    threshold = 15 * int(math.sqrt(n)) # Threshold for discoverability

    numOfRunsPerDataFile = 1    # Number of experiments to run per file

    dataPath = ''

    @staticmethod
    def dumpConfig(fileName):
        f = open(config.dataPath + fileName, "w")
        f.write('epsilon = ' + str(config.epsilon)+'\n')
        f.write('p = '+str(config.p)+'\n')
        f.write('n = ' + str(config.n)+'\n')
        f.write('w = ' + str(config.w)+'\n')
        f.write('l = ' + str(config.l)+'\n')
        f.write('No. of n-grams = ' + str(config.numNgrams)+'\n')
        f.write('Gram length = ' + str(config.gramLength)+'\n')
        f.write('Threshold = ' + str(config.threshold)+'\n')
        f.write('numOfRunsPerDataFile = ' + str(config.numOfRunsPerDataFile)+'\n')
