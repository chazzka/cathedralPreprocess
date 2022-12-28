import pandas
from datetime import datetime



def getNumberEight():
    return 8


def preprocess(data: pandas.DataFrame ):
    #filtered = data[(data['@iDevdAverageCurrent'] != 0)]
    filtered = data
    filtered['@dDevdCasZpravy'] = filtered['@dDevdCasZpravy'].apply(dateTimeToMilliseconds)
    return filtered


def dateTimeToMilliseconds(datetimeString):
    dt_obj = datetime.strptime(datetimeString,
                           '%Y-%m-%dT%H:%M:%S')
    millisec = dt_obj.timestamp() * 1000
    return millisec