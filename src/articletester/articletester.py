import numpy as np
import matplotlib.pyplot as plt
from itertools import *
from toolz import groupby

def plotDataWithMean(xyData):
    yValues = list(map(lambda x: x[1] ,xyData))
    mean = np.mean(yValues)
    grouped = groupby(lambda x: x[1] > mean, xyData)

    print(grouped)
    
    fig = plt.figure()
    ax1 = fig.add_subplot()

    ax1.scatter(*zip(*grouped[True]), c='green')
    ax1.scatter(*zip(*grouped[False]), c='blue')
    ax1.axhline(mean, c='red')
    plt.legend(loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Observed value")
    plt.show()
