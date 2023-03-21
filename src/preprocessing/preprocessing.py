import pandas
from datetime import datetime
import xmltodict as xtd
import logging
from datetime import datetime, timedelta
import sys


def getNumberEight():
    return 8


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


# for traning, we omit zeros
def filterOutZeros(preprocessed: list[dict], configArgs):
    return filter(lambda x: x[configArgs['averageColumnName']] != 0, preprocessed)


def preprocess(jsondata: dict, configArgs) -> list[dict]:
    prettyDict = convertToPrettyDict(jsondata)
    return preprocessAPIDict(prettyDict, configArgs)


def preprocessAPIDataFrame(data: pandas.DataFrame, configArgs):
    data_c = data.copy()
    data_c[configArgs['timeColumnName']] = data_c[configArgs['timeColumnName']].apply(
        apiDateTimeToMilliseconds)
    # nan as zero, all as float
    data_c[configArgs['averageColumnName']
           ] = data_c[configArgs['averageColumnName']].fillna(0).astype(float)
    return data_c


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
    # time to milisecond,
    tomili = list(map(
        mapcol(configArgs['timeColumnName'], apiDateTimeToMilliseconds), withoutNulls))
    # nan to 0
    # all as float
    return list(map(mapcol(configArgs['averageColumnName'], lambda x: float(x) or 0.0), tomili))


def preprocessCSVData(data: pandas.DataFrame):
    filtered = data[(data.ID_iot_device == 3) & (
        data['@iDevdAverageCurrent'] != 0)]
    filtered['@dDevdCasZpravy'] = filtered['@dDevdCasZpravy'].apply(
        CSVDateTimeToMilliseconds)
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


def convertToDF(json: dict) -> pandas.DataFrame:
    xmlres = xtd.parse(json['result'][2], force_list={'ROW'})

    try:
        dictRes = xmlres['DATAPACKET']['ROWDATA']['ROW']
    except IndexError:
        logging.error("No data found in json from API.")
        return pandas.DataFrame()

    return pandas.DataFrame.from_dict(dictRes)


def convertToPrettyDict(json: dict) -> list[dict]:
    xmlres = xtd.parse(json['result'][2], force_list={'ROW'})

    try:
        return xmlres['DATAPACKET']['ROWDATA']['ROW']
    except IndexError:
        logging.error("No data found in json from API.")
        return {}
