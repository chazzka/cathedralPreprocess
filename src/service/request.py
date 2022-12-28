import csv
import pandas
import json

import xml.etree.ElementTree as ET

import requests


def getCSVData(source: str) -> pandas.DataFrame:
    return pandas.read_csv(source ,usecols=['ID','@dDevdCasZpravy','ID_iot_device','@iDevdAverageCurrent'])


def fetchToJson(api_url: str):
    response = requests.get(api_url)
    json_response = json.loads(response.text)
    return json_response


def fetchToJsonWithHeaders(api_url: str, data: object, auth: tuple):
    response = requests.post(api_url, auth=auth, json=data)
    json_response = json.loads(response.text)
    return json_response

