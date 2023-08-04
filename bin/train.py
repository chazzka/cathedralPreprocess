from preprocessing.preprocessing import preprocess, filterOutZeros
from ai.trainer import doTrain, saveModel
import logging
import sys
import tomli
from service.request import fetchDataToDict
from random import sample

from datetime import datetime, timedelta


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


def getConfigFile(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


def getModel(data: dict, configArgs, aiArgs):
    preprocessed = preprocess(data, configArgs)
    # now training is done for non zeros data
    features = map(lambda x: x[configArgs["averageColumnName"]], preprocessed)
    noZeros = filter(lambda x:x != 0, features)
    noDuplicates = dict.fromkeys(noZeros)
    
    # noDuplicates = [89.0, 87.0, 90.0, 85.0, 85.0, 150.0,145.0,98.0, 86.0, 82.0, 87.0, 90.0, 91.0, 87.0, 84.0, 90.0, 86.0, 90.0, 90.0, 92.0, 87.0, 84.0, 86.0, 90.0, 91.0, 88.0, 89.0, 83.0, 86.0, 88.0, 84.0, 89.0, 92.0, 86.0, 85.0, 91.0, 91.0, 91.0, 87.0, 85.0, 89.0, 84.0, 83.0,110.0,130.0,67.0,68.0]
    noZeros = map(lambda x: [x], noDuplicates)
    
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
