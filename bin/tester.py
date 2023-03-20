import logging

from ai.trainer import loadModel, predict
from postprocessing.postprocessing import plotPredictedDataFrame
from mock.randomdatagenerator import createRandomDataFrame

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

    # evaluate model (accept dataframe and model, return trained dataframe)
    predictedDataFrame = predict(
        createRandomDataFrame(config),
        config["args"]["timeColumnName"],
        config["args"]["averageColumnName"],
        loadModel(config["args"]["modelPath"]),
        config["AI"])

    plotPredictedDataFrame(
            predictedDataFrame, config["args"]["timeColumnName"], config["args"]["averageColumnName"])

    print("done")
    sys.exit(0)
