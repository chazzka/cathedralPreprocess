import logging

from preprocessing.preprocessing import preprocess, getCurrentTimeAsDTString
from ai.trainer import loadModel, predict
from postprocessing.postprocessing import postprocess, plotPredictedDataFrame
from service.request import fetchToJsonWithHeaders

import sys
import tomli


def getConfigFile(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


def fetchDataToDict(serverConfig):
    data = {"_parameters": [serverConfig['apiDataIndentifier'], "", 0,
                            f"/sDeviceIdLst:\"{serverConfig['deviceIdLst']}\" /dDTFr:\"{getCurrentTimeAsDTString(daysSub=serverConfig['daystostrip'])}\" /dDTTo:\"{getCurrentTimeAsDTString()}\""]}

    res = fetchToJsonWithHeaders(
        serverConfig["url"], tuple(serverConfig["auth"]), data)
    return res


def postData(df, config, shouldSend=False):
    logging.info("starting postprocessing")
    data = {"_parameters": [config["server"]["apiDataIndentifier"], "", 0]}
    res = fetchToJsonWithHeaders(
        config["server"]["url"], tuple(config["server"]["auth"]), data)

    postprocessed = postprocess(df, config["args"], res)

    logging.info(postprocessed)

    # send result POST
    data = {"_parameters": [config["server"]
                            ["apiDataIndentifier"], postprocessed, 0]}

    if shouldSend:
        fetchToJsonWithHeaders(
            config["server"]["posturl"], tuple(config["server"]["auth"]), data)

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

    # prepare DataFrame with desired columns

    dataFrame = preprocess(fetchDataToDict(config["server"]), config["args"])

    # evaluate model (accept dataframe and model, return trained dataframe)
    predictedDataFrame = predict(
        dataFrame, config["args"]["timeColumnName"], config["args"]["averageColumnName"], loadModel(config["args"]["modelPath"]))

    if predictedDataFrame.empty:
        sys.exit(1)

    # postprocess - accept dataframe

    postData(predictedDataFrame, config, False)

    # optional: plot predicted dataframe
    plotPredictedDataFrame(
        predictedDataFrame, config["args"]["timeColumnName"], config["args"]["averageColumnName"])

    print("done")
    sys.exit(0)
