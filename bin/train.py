from preprocessing.preprocessing import preprocess
from ai.trainer import doTrain, saveModel
import logging
import sys
import tomli
from service.request import fetchDataToDict
from mock.randomdatagenerator import createRandomDataFrame

from datetime import datetime, timedelta


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


def getConfigFile(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


def getModel(data: dict, configArgs, aiArgs):
    #dataFrame = preprocess(data, configArgs)
    dataFrame = data
    features = dataFrame[[configArgs["timeColumnName"], configArgs["averageColumnName"]]].values.tolist()
    return doTrain(features, aiArgs)


if __name__ == "__main__":

    logging.basicConfig(filename='./logs/debug.log',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        encoding='utf-8', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    try:
        configFile = sys.argv[1]
    except IndexError:
        configFile = "config.toml"

    config = getConfigFile(configFile)

    data = fetchDataToDict(config["server"])

    data = createRandomDataFrame(config)

    linearModel = getModel(data, config["args"], config["AI"])

    saveModel(linearModel, f"{config['args']['newModelName']}.pckl")

    sys.exit(0)
