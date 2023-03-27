import json
import requests
import logging
from preprocessing.preprocessing import getNumberEight, getCurrentTimeAsDTString
import sys

def some():
    return 5 + getNumberEight()


def fetchDataToDict(serverConfig, dateTo):
    data = {"_parameters": [serverConfig['apiDataIndentifier'], "", 0,
                            f"/sDeviceIdLst:\"{serverConfig['deviceIdLst']}\" /dDTFr:\"{getCurrentTimeAsDTString(daysSub=serverConfig['daystostrip'])}\" /dDTTo:\"{dateTo}\""]}

    res = fetchToJsonWithHeaders(
        serverConfig["url"], tuple(serverConfig["auth"]), data)
    return res


def fetchToJson(api_url: str):
    response = requests.get(api_url)
    json_response = json.loads(response.text)
    logging.info("GET result:")
    logging.info(json_response)
    return json_response


def fetchToJsonWithHeaders(url, auth, data):
    response = requests.post(
        url, auth=auth, json=data)
    json_response = json.loads(response.text)
    logging.info("POST result:")
    logging.info(json_response)
    # error is unforutnatelly 200 OK with message: error
    if 'error' in json_response.keys():
        logging.error(json_response)
        sys.exit(1)
    return json_response
