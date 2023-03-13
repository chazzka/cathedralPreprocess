import logging

from preprocessing.preprocessing import preprocess
from ai.trainer import loadModel, predict
from postprocessing.postprocessing import postprocess, plotPredictedDataFrame
from service.request import fetchToJsonWithHeaders
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

    auth = config["auth"]

    # prepare testing dataframe



    plt.scatter(X3_space, [2*x + 250 for x in X3],
                marker="o", c=Y1, s=25, edgecolor="k")

    plt.show()

    testDataframe = pd.DataFrame({config["args"]["timeColumnName"]: list(X1[:, 0]) + X2_space + X3_space, config["args"]["averageColumnName"]: list(X1[:, 1]) + list(X2) + [x + 8 for x in X3.flatten()]})
    
    print(testDataframe)

    predictedDataFrame = predict(
        testDataframe, config["args"]["timeColumnName"], config["args"]["averageColumnName"], loadModel(config["args"]["modelPath"]))
    
    print(predictedDataFrame)

    if predictedDataFrame.empty:
        sys.exit(1)

    # postprocess - accept dataframe
    logging.info("starting postprocessing")

    # postprocessed = postprocess(
    #     predictedDataFrame, config)

    # logging.info(postprocessed)
    # # send result
    # data = {"_parameters": [config["args"]
    #                         ["apiDataIndentifier"], postprocessed, 0]}
    # res = fetchToJsonWithHeaders(
    #     config["server"]["posturl"], tuple(auth), data)

    # optional: plot predicted dataframe
    plotPredictedDataFrame(predictedDataFrame, config["args"]["timeColumnName"], config["args"]["averageColumnName"])

    print("done")
    sys.exit(0)
