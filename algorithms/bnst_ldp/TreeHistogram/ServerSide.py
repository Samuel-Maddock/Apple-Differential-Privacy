# Server side component of Count sketch, contains distribution and aggregation logic
from .config import config
import pandas as pd
import numpy as np
from .PrivCountSketch import countSketch as privCountSketch
import uuid
from collections import deque

# wordFrequency: The data file as a dataframe with the two columns ['word', 'trueFrequency']
# configFileName: File to dump the configuration parameters. Include expt info in the filename
# expResultFile: File to dump the experiment results as a .csv file

def runServerSide(wordFrequency, configFileName, exptResultFile, filePrefix=''):
    config.dumpConfig(filePrefix + configFileName)

    for run in range(config.numOfRunsPerDataFile):
        print('Running for iteration = ', run)
        counter = 0
        privCountSketch.sketchMatrix = np.zeros((config.l, config.w))
        for index, row in wordFrequency.iterrows():
            for i in range(row['trueFrequency']):
                counter += 1
                # if counter % 10000 == 0:
                #    print counter, row['word'], row['trueFrequency']

                privCountSketch.setSketchElement(row['word'])

        privFrequency = [0] * len(wordFrequency)
        privError = [0] * len(wordFrequency)
        for i, word in enumerate(wordFrequency['word']):
            privFrequency[i] = int(privCountSketch.getFreqEstimate(word))
            privError[i] = int(privFrequency[i] - wordFrequency['trueFrequency'][i])

        wordFrequency['privateFreq_run_freq' + str(run)] = privFrequency
        wordFrequency['privateFreq_run_error' + str(run)] = privError
        sketchFilePrefix = configFileName.replace('.txt', '') + '_run_'
        # Uncomment to write the sketch
        # PrivCountSketch.countSketch.writeSketchToFile(filePrefix + sketchFilePrefix + str(run) + '.npy')

    # wordFrequency['Mean_Freq'] = wordFrequency[list(range(2, 2 + 2 * config.numOfRunsPerDataFile, 2))].mean(axis=1)
    # wordFrequency['StdDev_Freq'] = wordFrequency[list(range(2, 2 + 2 * config.numOfRunsPerDataFile, 2))].std(axis=1)
    # wordFrequency['Error_Mean'] = wordFrequency[list(range(3, 3 + 2 * config.numOfRunsPerDataFile, 2))].mean(axis=1)
    # wordFrequency['Error_StdDev'] = wordFrequency[list(range(3, 3 + 2 * config.numOfRunsPerDataFile, 2))].std(axis=1)

    wordFrequency.to_csv(config.dataPath + filePrefix + exptResultFile, sep=',')


def runServerSideWordDiscovery(wordFrequency, configFileName, exptResultFile, filePrefix=''):
    config.dumpConfig(filePrefix + configFileName)
    wordLength = config.numNgrams * config.gramLength
    NGramSet = config.genEnglishNgrams(config.gramLength)

    precisionRecallMetricFileName = exptResultFile.replace('.csv', '_PR.csv')
    presRecDF = pd.DataFrame(['NumOfWords', 'Precision', 'Recall'], columns=['Measure'])

    for run in range(config.numOfRunsPerDataFile):
        print('Running for iteration = ', run)
        counter = 0
        privCountSketch.sketchMatrix = np.zeros((config.l, config.w))
        for index, row in wordFrequency.iterrows():
            for i in range(row['trueFrequency']):
                counter += 1
                # if counter % 10000 == 0: print counter, row['word'], row['trueFrequency']

                currentWord = row['word']
                if len(currentWord) <= wordLength:
                    currentWord += config.emptyChar * (wordLength - len(currentWord))
                else:
                    currentWord = currentWord[:wordLength]

                wordToSend = config.chooseRandomNGramPrefix(currentWord, config.gramLength)

                privCountSketch.setSketchElement(wordToSend)

        # Frequency estimation section
        scalingFactor = config.numNgrams
        listNGrams = config.genEnglishNgrams(config.gramLength)
        listNGrams = [s + config.emptyChar * (wordLength - len(s)) for s in listNGrams]
        wordQueue = deque(listNGrams)
        noisyFrequencies = {}
        tempCounter = 0
        while (wordQueue.__len__() != 0):
            currentPrefix = wordQueue.popleft()
            currentPrefixAfterStrippingEmpty = currentPrefix.replace(config.emptyChar, '')
            freqForCurrentPrefix = int(privCountSketch.getFreqEstimate(currentPrefix) * scalingFactor)

            if freqForCurrentPrefix < config.threshold:
                continue

            if len(currentPrefixAfterStrippingEmpty) == wordLength:
                noisyFrequencies[currentPrefixAfterStrippingEmpty] = freqForCurrentPrefix
                continue

            if tempCounter % 1000 == 0:
                print(
                'Running for iteration = ' + str(tempCounter) + ' , with queue length = ' + str(
                    wordQueue.__len__()) + ', current prefix = ' + currentPrefixAfterStrippingEmpty + ' current frequency=' + str(
                    freqForCurrentPrefix))
                print(wordQueue)
            tempCounter += 1

            for gram in NGramSet:
                toAdd = currentPrefixAfterStrippingEmpty + gram + config.emptyChar * (
                            wordLength - (len(currentPrefixAfterStrippingEmpty) + config.gramLength))
                wordQueue.append(toAdd)

        TP = 0.0
        FN = 0.0
        privFrequency = [0] * len(wordFrequency)
        print(len(wordFrequency))
        print(privFrequency)
        print(noisyFrequencies)
        for index, row in wordFrequency.iterrows():
            word = row['word']
            trueFrequency = row['trueFrequency']
            if word not in list(noisyFrequencies.keys()):
                privFrequency[index] = 0
                if trueFrequency > config.threshold:
                    FN += 1
            else:
                privFrequency[index] = noisyFrequencies[word]
                if trueFrequency > config.threshold:
                    TP += 1


        print(privFrequency)
        print(TP)
        print(noisyFrequencies.__len__())
        FP = noisyFrequencies.__len__() - TP
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)

        wordFrequency['privateFreq_run_' + str(run)] = privFrequency
        presRecDF['Run_' + str(run)] = [wordFrequency.__len__(), precision, recall]

        sketchFilePrefix = configFileName.replace('.txt', '') + '_run_'
        # Uncomment to write the sketch
        # PrivCountSketch.countSketch.writeSketchToFile(filePrefix + sketchFilePrefix + str(run) + '.npy')

    # wordFrequency['Mean_Freq'] = wordFrequency[list(range(2, 2 + config.numOfRunsPerDataFile))].mean(axis=1)
    # wordFrequency['StdDev_Freq'] = wordFrequency[list(range(2, 2 + config.numOfRunsPerDataFile))].std(axis=1)
    #
    # presRecDF['Mean_Estimate'] = presRecDF[list(range(1, 1 + config.numOfRunsPerDataFile))].mean(axis=1)
    # presRecDF['Std_Dev'] = presRecDF[list(range(1, 1 + config.numOfRunsPerDataFile))].std(axis=1)

    wordFrequency.to_csv(config.dataPath + filePrefix + exptResultFile, sep=',')
    presRecDF.to_csv(config.dataPath + filePrefix + precisionRecallMetricFileName, sep=',')

    for word in noisyFrequencies.keys():
        print(privCountSketch.getFreqEstimate(word))

    return noisyFrequencies
