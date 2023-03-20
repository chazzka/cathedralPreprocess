import logging

from preprocessing.preprocessing import preprocess, getCurrentTimeAsDTString
from ai.trainer import loadModel, predict
from postprocessing.postprocessing import postprocess, plotPredictedDataFrame
from service.request import fetchToJsonWithHeaders, fetchDataToDict

import sys
import tomli


def getConfigFile(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


def postData(predictedDataFrame, config, shouldSend=False):
    logging.info("starting postprocessing")
    data = {"_parameters": [config["server"]["apiDataIndentifier"], "", 0]}
    res = fetchToJsonWithHeaders(
        config["server"]["url"], tuple(config["server"]["auth"]), data)

    postprocessed = postprocess(predictedDataFrame, config["args"], res)

    logging.info(postprocessed)

    # send result POST
    data = {"_parameters": [config["server"]
                            ["apiDataIndentifier"], postprocessed, 0]}

    if shouldSend:
        fetchToJsonWithHeaders(
            config["server"]["posturl"], tuple(config["server"]["auth"]), data)
    else:
        plotPredictedDataFrame(
            predictedDataFrame, config["args"]["timeColumnName"], config["args"]["averageColumnName"])

    return postprocessed


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
        preprocess(fetchDataToDict(config["server"]), config["args"]), 
        config["args"]["timeColumnName"], 
        config["args"]["averageColumnName"], 
        loadModel(config["args"]["modelPath"]), 
        config["AI"])

    postData(predictedDataFrame, config, False)

    print("done")
    sys.exit(0)
