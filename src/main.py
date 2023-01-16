from preprocessing.preprocessing import preprocess
from ai.trainer import loadModel, predict
from postprocessing.postprocessing import postprocess, plotPredictedDataFrame
from service.request import fetchToJsonWithHeaders

import sys


if __name__ == "__main__":

    # TODO: later args
    shouldTrain = 0
    username = sys.argv[1]
    password = sys.argv[2]

    url = 'https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/GetRecordLst'
    posturl = 'https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/RecordLst'
    body = {"_parameters": ["iot_device_data", "", 0,
                            "/sDeviceIdLst:\"3\" /dDTFr:\"2021-05-16 10:25:41.000\" /dDTTo:\"2022-12-23 12:25:41.000\""]}
    auth = (username, password)

    averageColumnName = "@iDevdAverageCurrent"
    timeColumnName = "@dDevdCasZpravy"

# --------------------------------------

    # prepare DataFrame with desired columns
    dataFrame = preprocess(url, body, auth)

    # evaluate model (accept dataframe and model, return trained dataframe)
    predictedDataFrame = predict(dataFrame, timeColumnName, averageColumnName, loadModel('models/model.pckl'))

    # postprocess - accept dataframe, return whatever they want
    data = {"_parameters": ["iot_device_data", "", 0]}
    postprocessed = postprocess(predictedDataFrame, url, data, auth, '@ID', 'isCluster')

    print(postprocessed)
    # send result wherever they want
    res = fetchToJsonWithHeaders(posturl, data={"_parameters": ["iot_device_data", postprocessed, 0]}, auth=auth)
    #print(res)


    # optional: plot predicted dataframe
    #plotPredictedDataFrame(predictedDataFrame, timeColumnName, averageColumnName)
    
    sys.exit(1)