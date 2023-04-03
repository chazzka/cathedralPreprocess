from preprocessing.preprocessing import preprocess, filterOutZeros
from ai.trainer import doTrain, saveModel
import logging
import sys
import tomli
from service.request import fetchDataToDict

from datetime import datetime, timedelta


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


def getConfigFile(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


def getModel(data: dict, configArgs, aiArgs):
    preprocessed = preprocess(data, configArgs)
    
    # now training is done for non zeros data
    features = map(lambda x: [x[configArgs["timeColumnName"]], x[configArgs["averageColumnName"]]], preprocessed)
    noZeros = filterOutZeros(features, pos=1)
    
    #[[1,2], [4,0]]
    return doTrain(list(noZeros), aiArgs)


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

    data = fetchDataToDict(config["server"], config["server"]["date_to"] if config["server"]["date_to"] else getCurrentTimeAsDTString())

    linearModel = getModel(data, config["args"], config["AI"])

    saveModel(linearModel, f"{config['args']['newModelName']}.pckl")

    sys.exit(0)
