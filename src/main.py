from preprocessing.preprocessing import preprocess
from service.request import getCSVData, fetchToJson, jsonDestringify, fetchToJsonWithHeaders
from ai.trainer import doTrain
import pandas
import matplotlib.pyplot as plt
import numpy as np
import xmltodict as xtd


if __name__ == "__main__":

    data={"_parameters":["iot_device_data","",0,"/sDeviceIdLst:\"3\" /dDTFr:\"2022-12-16 10:25:41.000\" /dDTTo:\"2022-12-23 12:25:41.000\""]}
    auth=('a_ulrich@utb.cz', 'EcCNVU/dS76jpE938WxRHRGmjRM=')
    res = fetchToJsonWithHeaders('https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/GetRecordLst', data, auth)
    
    xmlres = xtd.parse(res['result'][2])
    dictres = xmlres['DATAPACKET']['ROWDATA']['ROW']

    data = pandas.DataFrame.from_dict(dictres)

    print(data)

    # data = getCSVData("./data/export.csv")

    filtered = preprocess(data)

    print(filtered)
    # assign row number to every bunch of data, so there is no noise
    filtered['ROW'] = np.arange(len(filtered))
    res = filtered[["ROW", "@iDevdAverageCurrent"]]

    trained = doTrain(res)

    df2 = res.assign(isAnomaly=trained)

    yesAnomaly = df2[(df2.isAnomaly == -1)]
    noAnomaly = df2[(df2.isAnomaly == 1)]

    print(df2)

    fig = plt.figure()
    ax1 = fig.add_subplot()

    ax1.scatter(yesAnomaly.ROW, yesAnomaly['@iDevdAverageCurrent'], label='anomalies')
    ax1.scatter(noAnomaly.ROW, noAnomaly['@iDevdAverageCurrent'], label='correct')
    plt.legend(loc='upper left')
    plt.show()
