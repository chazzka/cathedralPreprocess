import csv
import pandas


def getData(source: str) -> pandas.DataFrame:
    return pandas.read_csv(source ,usecols=['ID','Time','ID_iot_device','averageCurrent'])
