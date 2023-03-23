from datetime import datetime
import xmltodict as xtd
import logging
from datetime import datetime, timedelta
import sys


def getNumberEight():
    return 8


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


def filterOutZeros(preprocessed, pos):
    return filter(lambda x: x[pos] != 0, preprocessed)


def preprocess(jsondata: dict, configArgs) -> list[dict]:
    prettyDict = convertToPrettyDict(jsondata)
    return preprocessAPIDict(prettyDict, configArgs)


def mapcol(colname, function):
    return lambda x: x | {colname: function(x[colname])}


def replaceNoKeyWithValue(dic, key, value):
    if key not in dic:
        return dic | {key: value}
    else:
        return dic


def preprocessAPIDict(data: list[dict], configArgs):
    # first, non existant columns as 0.0
    withoutNulls = list(map(lambda dic: replaceNoKeyWithValue(
        dic, configArgs['averageColumnName'], 0.0), data))
    # time to milisecond
    tomili = list(map(
        mapcol(configArgs['timeColumnName'], apiDateTimeToMilliseconds), withoutNulls))
    # all as float
    return list(map(mapcol(configArgs['averageColumnName'], lambda x: float(x) or 0.0), tomili))



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


def convertToPrettyDict(json: dict) -> list[dict]:
    xmlres = xtd.parse(json['result'][2], force_list={'ROW'})

    try:
        return xmlres['DATAPACKET']['ROWDATA']['ROW']
    except:
        logging.error("No data found in json from API.")
        sys.exit(1)
