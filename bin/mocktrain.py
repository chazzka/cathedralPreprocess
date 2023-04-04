from preprocessing.preprocessing import filterOutZeros
from ai.trainer import doTrain, saveModel
import logging
import sys
import tomli
from mock.randomdatagenerator import createRandomData

from sklearn.ensemble import IsolationForest as model

from datetime import datetime, timedelta


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


def getConfigFile(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


def getModel(iterator, aiArgs, modelArgs):
    # now training is done for non zeros data
    noZeros = filterOutZeros(iterator, 1)
    #[[1,2], [4,5]]
    return doTrain(list(noZeros), aiArgs, modelArgs)


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

    linearModel = getModel(createRandomData(), config["anomaly"], model)

    saveModel(linearModel, f"{config['args']['newModelName']}.pckl")

    sys.exit(0)

