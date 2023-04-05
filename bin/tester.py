from ai.trainer import predict, fitPredict, getClusterLabels, doTrain
from postprocessing.postprocessing import plotXyWithPredicted
from mock.randomdatagenerator import createRandomData
import sys
import tomli
from itertools import product

import numpy as np

import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest as anomalymodel
from sklearn.cluster import DBSCAN as clustermodel

from articletester.articletester import *

def getConfigFile(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


def trainModel(iterator, aiArgs, model):
    # [[1,2], [4,5]]
    return doTrain(list(iterator), aiArgs, model)


if __name__ == "__main__":
    try:
        configFile = sys.argv[1]
    except IndexError:
        configFile = "config.toml"

    config = getConfigFile(configFile)

    # training data
    trainXyValues = list(createRandomData())

    plotDataWithMean(trainXyValues)
    
    sys.exit(1)

    # for test
    testXyValues = list(product(range(100), range(250)))

    trainedModel = trainModel(trainXyValues, config["anomaly"], anomalymodel)

    if config["AI"]["fitPredict"]:
        predictedList = list(fitPredict(
            trainXyValues,
            trainedModel
        ))
        plotXyWithPredicted(trainXyValues, predictedList)
        clusters = getClusterLabels(
            trainXyValues, predictedList, config["cluster"], clustermodel)
        plotXyWithPredicted(trainXyValues, clusters)
    else:
        predictedList = list(predict(
            testXyValues,
            trainedModel
        ))
        clusters = getClusterLabels(
            testXyValues, predictedList, config["cluster"], clustermodel)
        plotXyWithPredicted(testXyValues, predictedList)
        plotXyWithPredicted(testXyValues, clusters)
    

    print("done")
    sys.exit(0)
