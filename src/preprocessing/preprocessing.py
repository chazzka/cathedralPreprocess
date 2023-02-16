import pandas
from datetime import datetime
from dataclasses import dataclass
import xmltodict as xtd
from service.request import fetchToJsonWithHeaders

import logging
from datetime import datetime, timedelta

import sys


def getNumberEight():
    return 8


def getCurrentTimeAsDTString(time=datetime.now(), daysSub=0):
    return (time - timedelta(days=int(daysSub))).strftime('%Y-%m-%d %H:%M:%S')


def preprocess(config) -> pandas.DataFrame:
    args = config["args"]
    data = {"_parameters": [args['apiDataIndentifier'], "", 0,
                            f"/sDeviceIdLst:\"{args['deviceIdLst']}\" /dDTFr:\"{getCurrentTimeAsDTString(daysSub=args['daystostrip'])}\" /dDTTo:\"{getCurrentTimeAsDTString()}\""]}

    res = fetchToJsonWithHeaders(
        config["server"]["url"], tuple(config["auth"]), data)

    dataFrameRes = convertToDF(res)
    return preprocessAPIDataFrame(dataFrameRes, args)


def preprocessAPIDataFrame(data: pandas.DataFrame, configArgs):
    idColumn = data[configArgs['idColumnName']]
    timeColumn = data[configArgs['timeColumnName']].apply(
        apiDateTimeToMilliseconds)
    averageColumn = data[configArgs['averageColumnName']].astype(float)
    filtered = pandas.DataFrame(
        data={configArgs['idColumnName']: idColumn, configArgs['timeColumnName']: timeColumn, configArgs['averageColumnName']: averageColumn})
    return filtered


def preprocessCSVData(data: pandas.DataFrame):
    filtered = data.dropna(subset=['@iDevdAverageCurrent'])
    filtered = filtered[(filtered['@iDevdAverageCurrent'] != 0)]

    filtered['@dDevdCasZpravy'] = filtered['@dDevdCasZpravy']
    print(filtered)
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
