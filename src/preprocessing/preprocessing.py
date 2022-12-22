import pandas

def getNumberEight():
    return 8


def preprocess(data: pandas.DataFrame ):
    return data[(data.ID_iot_device == 3) & (data.averageCurrent != 0)]

