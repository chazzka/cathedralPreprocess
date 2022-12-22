from preprocessing.preprocessing import preprocess
from http.request import getData
from ai.trainer import doTrain
import pandas
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    data = getData("./data/export.csv")

    filtered = preprocess(data)

    # assign row number to every bunch of data, so there is no noise
    filtered['ROW'] = np.arange(len(filtered))
    res = filtered[["ROW", "averageCurrent"]]

    print(res)
    trained = doTrain(res)

    df2 = res.assign(isAnomaly=trained)

    yesAnomaly = df2[(df2.isAnomaly == -1)]
    noAnomaly = df2[(df2.isAnomaly == 1)]

    print(yesAnomaly)

    fig = plt.figure()
    ax1 = fig.add_subplot()

    ax1.scatter(yesAnomaly.ROW, yesAnomaly.averageCurrent, label='anomalies')
    ax1.scatter(noAnomaly.ROW, noAnomaly.averageCurrent, label='correct')
    plt.legend(loc='upper left')
    plt.show()
