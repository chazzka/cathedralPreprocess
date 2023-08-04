from sklearn.ensemble import IsolationForest
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
    return map(lambda x,y: 1 if x == 0 else y, df, prediction)


def getClusterLabels(xyValues, predicted, aiArgs):
    anomalies = map(lambda x: -x, predicted)
    
    return findCluster(xyValues,anomalies,aiArgs)


def doTrain(X_train, aiArgs):
    # return forestTrain(X_train, aiArgs["contamination"])
    return localOutlierTrain(X_train)

# 1 - not a cluster
# 0 - is a cluster
# SAMPLE WEIGHT - DB scan can ignore points with minus weight
def findCluster(X_Train: Sequence[float], sample_weight, aiArgs):
    return findClusterDBScan(X_Train, sample_weight, aiArgs["eps"], aiArgs["min_samples"])
    # return findClusterKMeans(X_Train, sample_weight)


def findClusterDBScan(X_train: Sequence[float], sample_weight, eps=7, min_samples=10):
    return DBSCAN(eps=eps, min_samples=min_samples).fit_predict(list(X_train), sample_weight=list(sample_weight))


def findClusterKMeans(X_train, sample_weight):
    return KMeans(n_clusters=2, random_state=0, n_init="auto", algorithm="lloyd").fit_predict(list(X_train), sample_weight=list(sample_weight))


def forestTrain(X_train, contamination=0.02):
    clf = IsolationForest(max_samples='auto', random_state=0,
                          contamination=contamination)
    return clf.fit(X_train)


def svmTrain(X_train):
    return OneClassSVM(kernel='linear', nu=0.1).fit(X_train)


def sdgSvmTrain(X_train):
    return SGDOneClassSVM().fit(X_train)


def ellipticTrain(X_train):
    return EllipticEnvelope(random_state=0, assume_centered=False, contamination=0.05).fit(X_train)


def ellipticFitPredict(X_train):
    return EllipticEnvelope(random_state=0, assume_centered=False, contamination=0.1).fit_predict(X_train)


def localOutlierTrain(X_train):
    return LocalOutlierFactor(novelty=True).fit(X_train)


def saveModel(model, filename):
    logging.info(f"saving model {filename}")
    pickle.dump(model, open(f'models/{filename}', 'wb'))


def loadModel(path):
    return pickle.load(open(path, 'rb'))
