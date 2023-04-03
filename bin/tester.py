import logging

from ai.trainer import loadModel, predict, fitPredict, getClusterLabels, doAnomalyTrain
from postprocessing.postprocessing import plotXyWithPredicted
from mock.randomdatagenerator import createRandomData

import sys
import tomli


def getConfigFile(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


if __name__ == "__main__":

    logging.basicConfig(filename='./logs/debug.log',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        encoding='utf-8', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("starting script")

    try:
        configFile = sys.argv[1]
    except IndexError:
        configFile = "config.toml"

    config = getConfigFile(configFile)

    xyValues = list(createRandomData())

    if config["AI"]["predictAnomalies"]:
        if config["AI"]["fitPredict"]:
            predictedList = fitPredict(
                xyValues,
                doAnomalyTrain(
                    xyValues, config["anomaly"], config["anomalymodel"])
            )
        else:
            predictedList = predict(
                xyValues,
                loadModel(config["args"]["modelPath"])
            )
    else:
        predictedList = map(lambda x: -1, xyValues)
        print(predictedList)
        print("ano")

    if config["AI"]["predictClusters"]:
        clusters = getClusterLabels(
            xyValues, predictedList, config["cluster"], config["clustermodel"])
        plotXyWithPredicted(xyValues, clusters)
    else:
        plotXyWithPredicted(xyValues, list(predictedList))

    print("done")
    sys.exit(0)
