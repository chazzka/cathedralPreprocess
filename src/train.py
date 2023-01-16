from preprocessing.preprocessing import preprocess
from ai.trainer import doTrain, saveModel
import logging
import sys

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

    idColumnName = sys.argv[6]  # @ID
    averageColumnName = sys.argv[7]  # @iDevdAverageCurrent
    timeColumnName = sys.argv[8]  # @dDevdCasZpravy
    apiDataIndentifier = sys.argv[9]  # iot_device_data
    deviceIdLst = sys.argv[10]  # 3

    newModelName = sys.argv[11]

    body = {"_parameters": [apiDataIndentifier, "", 0,
                            f"/sDeviceIdLst:\"{deviceIdLst}\" /dDTFr:\"{getCurrentTimeAsDTString(daysSub=daystostrip)}\" /dDTTo:\"{getCurrentTimeAsDTString()}\""]}
    auth = (username, password)

    desiredColumns = {'idColumnName': idColumnName,
                      'averageColumnName': averageColumnName, 'timeColumnName': timeColumnName}

    filtered = preprocess(url, body, auth, desiredColumns)
    # fitting elispoid, take only desired feature
    res = filtered[[averageColumnName]]
    linearTrained = doTrain(res)
    filename = f'{newModelName}.pckl'
    saveModel(linearTrained, filename)

    logging.error("no cluster found")
    sys.exit(1)
