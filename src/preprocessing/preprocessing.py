import pandas
from datetime import datetime
from dataclasses import dataclass
import xmltodict as xtd
from service.request import fetchToJsonWithHeaders


def getNumberEight():
    return 8


def preprocess(url, data, auth):
    res = fetchToJsonWithHeaders(
        url, data, auth)

    dataFrameRes = convertToDF(res)
    return preprocessAPIData(dataFrameRes)


def preprocessAPIData(data: pandas.DataFrame):
    # filtered = data[(data['@iDevdAverageCurrent'] != 0)]
    timeColumn = data['@dDevdCasZpravy'].apply(apiDateTimeToMilliseconds)
    averageColumn = data['@iDevdAverageCurrent'].astype(float)
    filtered = pandas.DataFrame(
        data={'@dDevdCasZpravy': timeColumn, '@iDevdAverageCurrent': averageColumn})
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


@dataclass(frozen=True)
class Row:
    id: int
    bDevdAvgCurrentAnomaly: bool


def prepareRowXML(row: Row):
    return f'<ROW ID=\"{row.id}\" bDevdAvgCurrentAnomaly=\"{row.bDevdAvgCurrentAnomaly}\"/>'


def prepareRowsXML(idAnomalyDics: list[Row]):
    return list(map(prepareRowXML, idAnomalyDics))


def convertToDF(json: dict):
    xmlres = xtd.parse(json['result'][2])
    dictRes = xmlres['DATAPACKET']['ROWDATA']['ROW']
    return pandas.DataFrame.from_dict(dictRes)
