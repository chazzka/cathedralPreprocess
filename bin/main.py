import logging.config

from preprocessing.preprocessing import preprocess, getCurrentTimeAsDTString
from ai.trainer import loadModel, predict, getClusterLabels
from postprocessing.postprocessing import postprocess, plotXyWithPredicted
from service.request import fetchToJsonWithHeaders, fetchDataToDict

import sys
import tomli


def getTomlFileToDict(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


def postData(xyArray, predicted, dataFromApi, config, shouldSend=False):
    print(predicted)
    if shouldSend:
        data = {"_parameters": [config["server"]["apiDataIndentifier"], "", 0]}

        headers = fetchToJsonWithHeaders(
            config["server"]["url"], tuple(config["server"]["auth"]), data
        )

        postprocessed = postprocess(
            map(lambda x: x[config["args"]["idColumnName"]], dataFromApi),
            map(lambda x: x != -1 or 1, predicted), headers
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

    dataFromApi = fetchDataToDict(config["server"])

    preprocessedDict = preprocess(dataFromApi, config["args"])

    xyTupleList = list(map(lambda x: (
        x[config["args"]["timeColumnName"]], x[config["args"]["averageColumnName"]]), preprocessedDict))

    # evaluate model (accept dataframe and model, return trained dataframe)
    predictedIterator = predict(
        xyTupleList,
        loadModel(config["args"]["modelPath"]),
    )

    clustersLabels = getClusterLabels(xyTupleList, predictedIterator, config["AI"])

    postData(xyTupleList, clustersLabels, preprocessedDict, config, False)

    print("done")
    sys.exit(0)
