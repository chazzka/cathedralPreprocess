import logging

from preprocessing.preprocessing import preprocess, preprocessCSVData
from ai.trainer import loadModel, predict
from postprocessing.postprocessing import postprocess, plotPredictedDataFrame
from service.request import fetchToJsonWithHeaders

import sys
import tomli
import pandas as pd


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

    auth = config["auth"]

    # prepare DataFrame with desired columns

    #dataFrame = preprocess(config)
    dataFrame = preprocessCSVData(pd.read_csv('data/export.csv'))

    # evaluate model (accept dataframe and model, return trained dataframe)
    predictedDataFrame = predict(
        dataFrame, config["args"]["timeColumnName"], config["args"]["averageColumnName"], loadModel(config["args"]["modelPath"]))

    if predictedDataFrame.empty:
        sys.exit(1)

    # postprocess - accept dataframe
    logging.info("starting postprocessing")

    #postprocessed = postprocess(predictedDataFrame, config)

    #logging.info(postprocessed)

    # send result
    data = {"_parameters": [config["args"]["apiDataIndentifier"], "", 0]}
    #res = fetchToJsonWithHeaders(config["server"]["posturl"], tuple(auth), data)

    # optional: plot predicted dataframe
    print(predictedDataFrame)
    plotPredictedDataFrame(predictedDataFrame, config["args"]["timeColumnName"], config["args"]["averageColumnName"])

    print("done")
    sys.exit(0)
