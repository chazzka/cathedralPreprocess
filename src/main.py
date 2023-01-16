from preprocessing.preprocessing import preprocess
from ai.trainer import loadModel, predict
from postprocessing.postprocessing import postprocess, plotPredictedDataFrame
from service.request import fetchToJsonWithHeaders

import sys
import time
from datetime import datetime, timedelta


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":

    # TODO: later args
    shouldTrain = 0
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

# --------------------------------------

    # prepare DataFrame with desired columns
    dataFrame = preprocess(url, body, auth)

    # evaluate model (accept dataframe and model, return trained dataframe)
    predictedDataFrame = predict(
        dataFrame, timeColumnName, averageColumnName, loadModel('models/model.pckl'))

    if predictedDataFrame.empty:
        sys.exit(1)

    # postprocess - accept dataframe, return whatever they want
    data = {"_parameters": ["iot_device_data", "", 0]}
    postprocessed = postprocess(
        predictedDataFrame, url, data, auth, '@ID', 'isCluster')

    print(postprocessed)
    # send result wherever they want
    res = fetchToJsonWithHeaders(posturl, data={"_parameters": [
                                 "iot_device_data", postprocessed, 0]}, auth=auth)

    # optional: plot predicted dataframe
    # plotPredictedDataFrame(predictedDataFrame, timeColumnName, averageColumnName)

    sys.exit(1)
