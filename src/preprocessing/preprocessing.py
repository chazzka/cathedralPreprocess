import pandas
from datetime import datetime
from dataclasses import dataclass
import xmltodict as xtd
from service.request import fetchToJsonWithHeaders

import logging

def getNumberEight():
    return 8


def preprocess(url, data, auth, desiredColumns) -> pandas.DataFrame:
    res = fetchToJsonWithHeaders(
        url, data, auth)

    dataFrameRes = convertToDF(res)
    return preprocessAPIDataFrame(dataFrameRes, desiredColumns)


def preprocessAPIDataFrame(data: pandas.DataFrame, desiredColumns):
    idColumn = data[desiredColumns['idColumnName']]
    timeColumn = data[desiredColumns['timeColumnName']].apply(apiDateTimeToMilliseconds)
    averageColumn = data[desiredColumns['averageColumnName']].astype(float)
    filtered = pandas.DataFrame(
        data={desiredColumns['idColumnName']: idColumn, desiredColumns['timeColumnName']: timeColumn, desiredColumns['averageColumnName']: averageColumn})
    return filtered


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
