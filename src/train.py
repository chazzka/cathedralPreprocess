from preprocessing.preprocessing import preprocess
from ai.trainer import doTrain, saveModel
import logging
import sys
import tomli

from datetime import datetime, timedelta


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


def getConfigFile(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


if __name__ == "__main__":

    logging.basicConfig(filename='logs/debug.log',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        encoding='utf-8', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    try:
        configFile = sys.argv[1]
    except IndexError:
        configFile = "config.toml"

    config = getConfigFile(configFile)

    averageColumnName = config["args"]["averageColumnName"]  # @iDevdAverageCurrent
    newModelName = config["args"]["newModelName"]

    filtered = preprocess(config)
    # fitting elispoid, take only desired feature
    res = filtered[[averageColumnName]]
    linearTrained = doTrain(res)
    filename = f'{newModelName}.pckl'

    logging.info(f"saving model {newModelName}")
    saveModel(linearTrained, filename)

    sys.exit(1)
