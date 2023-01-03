from preprocessing.preprocessing import preprocessCSVData, prepareRowsXML, Row, preprocess
from service.request import getCSVData, fetchToJsonWithHeaders
from ai.trainer import doTrain, saveModel, loadModel, findCluster

import sys
import pandas
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":

    # TODO: later args
    username = sys.argv[1]
    password = sys.argv[2]

    url = 'https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/GetRecordLst'
    data = {"_parameters": ["iot_device_data", "", 0,
                            "/sDeviceIdLst:\"3\" /dDTFr:\"2022-08-16 10:25:41.000\" /dDTTo:\"2022-12-23 12:25:41.000\""]}
    auth = (username, password)

    averageColumnName = "@iDevdAverageCurrent"
    timeColumnName = "@dDevdCasZpravy"

    filtered = preprocessCSVData(getCSVData("./data/export.csv"))
    # fitting elispoid, take only desired feature
    res = filtered[[averageColumnName]]
    linearTrained = doTrain(res)
    saveModel(linearTrained)

    # TODO: SAVE AND EXIT, maybe show graph?

    prediction = linearTrained.predict(res)

    print(prediction)

    df2 = filtered[[timeColumnName, averageColumnName]].assign(
        isAnomaly=prediction)

    yesAnomaly = df2[(df2.isAnomaly == -1)]
    noAnomaly = df2[(df2.isAnomaly == 1)]

    dfAnomalies = yesAnomaly[[timeColumnName, averageColumnName]]

    try:
        cluster = findCluster(dfAnomalies)
    except:
        print("no cluster found")
        sys.exit(1)

    clusterLabeledDf = dfAnomalies.assign(isCluster=cluster)

    # here send post

    # get header metadata

    # TODO: POSTPROCESS

    # the rest is not a cluster (just for pretty printing)
    toMerge = noAnomaly[[timeColumnName,
                         averageColumnName]].assign(isCluster=1)

    merged = pandas.concat(
        [clusterLabeledDf, toMerge],
        axis=0,
        join="outer",
        ignore_index=False,
        keys=None,
        levels=None,
        names=None,
        verify_integrity=False,
        copy=True,
    )

    fig = plt.figure()
    ax1 = fig.add_subplot()

    yesCluster = merged[(merged.isCluster == 0)]
    noCluster = merged[(merged.isCluster == 1)]

    ax1.scatter(yesCluster[timeColumnName],
                yesCluster[averageColumnName], label='cluster of anomalies')
    ax1.scatter(noCluster[timeColumnName],
                noCluster[averageColumnName], label='correct')
    plt.legend(loc='upper left')
    plt.show()
