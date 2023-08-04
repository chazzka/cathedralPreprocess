import logging.config

from preprocessing.preprocessing import preprocess, getCurrentTimeAsDTString
from ai.trainer import loadModel, predict, getClusterLabels
from postprocessing.postprocessing import postprocess, plotXyWithPredicted
from service.request import fetchToJsonWithHeaders, fetchDataToDict
import numpy as np
import matplotlib.pyplot as plt
import sys
import tomli


def getTomlFileToDict(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


def postData(xyArray, predicted, dataFromApi, config, shouldSend=False):
    if shouldSend:
        data = {"_parameters": [config["server"]["apiDataIndentifier"], "", 0]}

        headers = fetchToJsonWithHeaders(
            config["server"]["url"], tuple(config["server"]["auth"]), data
        )

        postprocessed = postprocess(
            map(lambda x: x[config["args"]["idColumnName"]], dataFromApi),
            map(lambda x: 1 if x == -1 else 0, predicted), headers
        )

        # send result POST
        data = {"_parameters": [config["server"]
                                ["apiDataIndentifier"], postprocessed, 0]}

        fetchToJsonWithHeaders(
            config["server"]["posturl"], tuple(config["server"]["auth"]), data)
    else:
        plotXyWithPredicted(xyArray, predicted)

    return 0


if __name__ == "__main__":

    logging.config.dictConfig(getTomlFileToDict("loggingconfig.toml"))

    try:
        configFile = sys.argv[1]
    except IndexError:
        configFile = "config.toml"

    config = getTomlFileToDict(configFile)

    dataFromApi = fetchDataToDict(config["server"], config["server"]["date_to"] if config["server"]["date_to"] else getCurrentTimeAsDTString())
    preprocessedDict = preprocess(dataFromApi, config["args"])

    xTupleList = np.array(list(map(lambda x: (
        x[config["args"]["averageColumnName"]]), preprocessedDict))).reshape(-1,1)

    # evaluate model (accept dataframe and model, return trained dataframe)
    predictedIterator = predict(
        xTupleList ,
        loadModel(config["args"]["modelPath"]),
    )
    originalList = list(map(lambda x: (x[config["args"]["timeColumnName"]], x[config["args"]["averageColumnName"]]), preprocessedDict))
    # plotXyWithPredicted(originalList, list(map(lambda x: "#ff7f0e" if x == -1 else "#2ca02c", predictedIterator)))
    
    clustersLabels = getClusterLabels(
        xTupleList , predictedIterator, config["AI"])
    
    postData(xTupleList , clustersLabels, preprocessedDict, config, True)
    # plotXyWithPredicted(originalList, list(map(lambda x: "#ff7f0e" if x == -1 else "#2ca02c", clustersLabels)))
    print("done")
    sys.exit(0)
