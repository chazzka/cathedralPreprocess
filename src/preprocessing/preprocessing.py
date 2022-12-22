import pandas
from datetime import datetime



def getNumberEight():
    return 8


def preprocess(data: pandas.DataFrame ):
    filtered = data[(data.ID_iot_device == 3) & (data.averageCurrent != 0)]
    filtered['Time'] = filtered['Time'].apply(dateTimeToMilliseconds)
    return filtered


def dateTimeToMilliseconds(datetimeString):
    dt_obj = datetime.strptime(datetimeString,
                           '%Y-%m-%d %H:%M:%S.%f')
    millisec = dt_obj.timestamp() * 1000
    return millisec