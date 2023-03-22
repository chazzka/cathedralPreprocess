import logging

from ai.trainer import loadModel, predict, getClusters
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
    predictedList = predict(
        xyValues,
        loadModel(config["args"]["modelPath"])
    )

    clusters = getClusters(xyValues, predictedList, config["AI"])

    plotXyWithPredicted(xyValues, clusters)

    print("done")
    sys.exit(0)
