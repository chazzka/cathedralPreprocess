#from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.linear_model import SGDOneClassSVM
from typing import Sequence
from itertools import *

import pickle
import logging


# accept list of tuples (x,y), return predicted array
# returns list[-1=anomalies/1=no anomalies]
def predict(df, model):
    prediction = model.predict(list(df))
    # if observed value was 0.0, assign 1 - no anomaly
    return map(lambda x,y: x[1] == 0 or y, df, prediction)

def fitPredict(df, model):
    prediction = model.fit_predict(list(df))
    # if observed value was 0.0, assign 1 - no anomaly
    return map(lambda x,y: x[1] == 0 or y, df, prediction)


def getClusterLabels(xyValues, predicted, clusterArgs, modelArgs):
    anomalies = map(lambda x: -x, predicted)
    model = getattr(__import__(modelArgs["path"], fromlist=[modelArgs["what"]]), modelArgs["what"])
    return model(**clusterArgs).fit_predict(list(xyValues), sample_weight=list(anomalies))


def doAnomalyTrain(X_train, anomalyArgs, modelArgs):
    model = getattr(__import__(modelArgs["path"], fromlist=[modelArgs["what"]]), modelArgs["what"])
    return model(**anomalyArgs).fit(X_train)



def saveModel(model, filename):
    logging.info(f"saving model {filename}")
    pickle.dump(model, open(f'models/{filename}', 'wb'))


def loadModel(path):
    return pickle.load(open(path, 'rb'))
