from preprocessing.preprocessing import preprocessCSVData
from service.request import getCSVData
from ai.trainer import doTrain, saveModel, findCluster

import logging
import sys
import pandas
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime, timedelta


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":

    logging.basicConfig(filename='logs/debug.log',
                        encoding='utf-8', level=logging.DEBUG)

    # TODO: later args
    username = sys.argv[1]
    password = sys.argv[2]

    daystostrip = sys.argv[3]

    # url = 'https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/GetRecordLst'
    url = sys.argv[4]
    # posturl = 'https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/RecordLst'
    posturl = sys.argv[5]

    body = {"_parameters": ["iot_device_data", "", 0,
                            f"/sDeviceIdLst:\"3\" /dDTFr:\"{getCurrentTimeAsDTString(daysSub=daystostrip)}\" /dDTTo:\"{getCurrentTimeAsDTString()}\""]}
    auth = (username, password)

    averageColumnName = "@iDevdAverageCurrent"
    timeColumnName = "@dDevdCasZpravy"

    filtered = preprocessCSVData(getCSVData("./data/export.csv"))
    # fitting elispoid, take only desired feature
    res = filtered[[averageColumnName]]
    linearTrained = doTrain(res)
    saveModel(linearTrained)

    logging.error("no cluster found")
    sys.exit(1)
