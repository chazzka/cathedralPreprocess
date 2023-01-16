import logging

from preprocessing.preprocessing import preprocess
from ai.trainer import loadModel, predict
from postprocessing.postprocessing import postprocess, plotPredictedDataFrame
from service.request import fetchToJsonWithHeaders

import sys
from datetime import datetime, timedelta


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":

    logging.basicConfig(filename='logs/debug.log',
                        encoding='utf-8', level=logging.DEBUG)

    username = sys.argv[1]
    password = sys.argv[2]
    daystostrip = sys.argv[3]

    url = sys.argv[4]
    posturl = sys.argv[5]

    idColumnName = sys.argv[6]  # @ID
    averageColumnName = sys.argv[7]  # @iDevdAverageCurrent
    timeColumnName = sys.argv[8]  # @dDevdCasZpravy
    apiDataIndentifier = sys.argv[9]  # iot_device_data
    deviceIdLst = sys.argv[10]  # 3
    modelPath = sys.argv[11] # models/model.pckl

    body = {"_parameters": [apiDataIndentifier, "", 0,
                            f"/sDeviceIdLst:\"{deviceIdLst}\" /dDTFr:\"{getCurrentTimeAsDTString(daysSub=daystostrip)}\" /dDTTo:\"{getCurrentTimeAsDTString()}\""]}
    auth = (username, password)

    desiredColumns = {'idColumnName': idColumnName,
                      'averageColumnName': averageColumnName, 'timeColumnName': timeColumnName}

    # prepare DataFrame with desired columns
    dataFrame = preprocess(url, body, auth, desiredColumns)

    # evaluate model (accept dataframe and model, return trained dataframe)
    predictedDataFrame = predict(
        dataFrame, timeColumnName, averageColumnName, loadModel(modelPath))

    if predictedDataFrame.empty:
        sys.exit(1)

    # postprocess - accept dataframe
    logging.info("starting postprocessing")
    data = {"_parameters": ["iot_device_data", "", 0]}
    postprocessed = postprocess(
        predictedDataFrame, url, data, auth, '@ID', 'isCluster')

    logging.info(postprocessed)

    # send result
    res = fetchToJsonWithHeaders(posturl, data={"_parameters": [
                                 "iot_device_data", postprocessed, 0]}, auth=auth)

    # optional: plot predicted dataframe
    # plotPredictedDataFrame(predictedDataFrame, timeColumnName, averageColumnName)

    sys.exit(1)
