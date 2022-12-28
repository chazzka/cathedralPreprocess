
from preprocessing.preprocessing import preprocessAPIData, preprocessCSVData
from service.request import getCSVData, fetchToJsonWithHeaders
from ai.trainer import doTrain, saveModel, loadModel

import sys
import pandas
import matplotlib.pyplot as plt
import numpy as np
import xmltodict as xtd


if __name__ == "__main__":

    # TODO: later args
    shouldTrain = 0
    username = sys.argv[1]
    password = sys.argv[2]

    averageColumnName = "@iDevdAverageCurrent"
    timeColumnName = "@dDevdCasZpravy"

    if shouldTrain == 1:
        csvData = getCSVData("./data/export.csv")
        filtered = preprocessCSVData(csvData)
        res = filtered[[timeColumnName, averageColumnName]]

        trained = doTrain(res)
        saveModel(trained)
        trained = trained.predict(res)

    if shouldTrain == 0:
        data = {"_parameters": ["iot_device_data", "", 0,
                                "/sDeviceIdLst:\"3\" /dDTFr:\"2022-2-16 10:25:41.000\" /dDTTo:\"2022-12-23 12:25:41.000\""]}
        auth = (username, password)
        res = fetchToJsonWithHeaders(
            'https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/GetRecordLst', data, auth)

        xmlres = xtd.parse(res['result'][2])
        dictres = xmlres['DATAPACKET']['ROWDATA']['ROW']

        data = pandas.DataFrame.from_dict(dictres)
        filtered = preprocessAPIData(data)
        res = filtered[[timeColumnName, averageColumnName]]

        trained = loadModel('models/model.pckl')
        trained = trained.predict(res)

    df2 = res.assign(isAnomaly=trained)

    yesAnomaly = df2[(df2.isAnomaly == -1)]
    noAnomaly = df2[(df2.isAnomaly == 1)]

    print(df2)

    fig = plt.figure()
    ax1 = fig.add_subplot()

    ax1.scatter(yesAnomaly[timeColumnName],
                yesAnomaly[averageColumnName], label='anomalies')
    ax1.scatter(noAnomaly[timeColumnName],
                noAnomaly[averageColumnName], label='correct')
    plt.legend(loc='upper left')
    plt.show()
