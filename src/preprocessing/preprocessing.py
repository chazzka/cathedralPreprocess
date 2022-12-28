import pandas
from datetime import datetime



def getNumberEight():
    return 8


def preprocessAPIData(data: pandas.DataFrame ):
    filtered = data[(data['@iDevdAverageCurrent'] != 0)]
    filtered = data
    filtered['@dDevdCasZpravy'] = filtered['@dDevdCasZpravy'].apply(apiDateTimeToMilliseconds)
    filtered['@iDevdAverageCurrent'] = filtered['@iDevdAverageCurrent'].astype(float)
    return filtered


def preprocessCSVData(data: pandas.DataFrame ):
    filtered = data[(data.ID_iot_device == 3) & (data['@iDevdAverageCurrent'] != 0)]
    filtered['@dDevdCasZpravy'] = filtered['@dDevdCasZpravy'].apply(CSVDateTimeToMilliseconds)
    return filtered


def apiDateTimeToMilliseconds(datetimeString):
    dt_obj = datetime.strptime(datetimeString,
                           '%Y-%m-%dT%H:%M:%S')
    millisec = dt_obj.timestamp() * 1000
    return millisec


def apiDateTimeToMilliseconds(datetimeString):
    dt_obj = datetime.strptime(datetimeString,
                           '%Y-%m-%dT%H:%M:%S')
    millisec = dt_obj.timestamp() * 1000
    return millisec


def CSVDateTimeToMilliseconds(datetimeString):
    dt_obj = datetime.strptime(datetimeString,
                           '%Y-%m-%d %H:%M:%S.%f')
    millisec = dt_obj.timestamp() * 1000
    return millisec