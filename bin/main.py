import logging

from preprocessing.preprocessing import preprocess, getCurrentTimeAsDTString
from ai.trainer import loadModel, predict, getClusters
from postprocessing.postprocessing import postprocess, plotXyWithPredicted
from service.request import fetchToJsonWithHeaders, fetchDataToDict

import sys
import tomli


def getConfigFile(path):
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
            map(lambda x: x != -1 or 1, predicted), headers
        )

        print(postprocessed)
        sys.exit(1)
        # send result POST
        data = {"_parameters": [config["server"]
                                ["apiDataIndentifier"], postprocessed, 0]}

        fetchToJsonWithHeaders(
            config["server"]["posturl"], tuple(config["server"]["auth"]), data)
    else:
        plotXyWithPredicted(xyArray, predicted)

    return 0


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

    dataFromApi = fetchDataToDict(config["server"])

    preprocessedDict = preprocess(dataFromApi, config["args"])

    xyTupleList = list(map(lambda x: (
        x[config["args"]["timeColumnName"]], x[config["args"]["averageColumnName"]]), preprocessedDict))

    # evaluate model (accept dataframe and model, return trained dataframe)
    predictedIterator = predict(
        xyTupleList,
        loadModel(config["args"]["modelPath"]),
    )

    clusters = getClusters(xyTupleList, predictedIterator, config["AI"])

    # print(len(clusters))
    print(clusters)

    # TODO: donut je at ti vygeneruji nejake clustery

    postData(xyTupleList, clusters, preprocessedDict, config, False)

    print("done")
    sys.exit(0)
