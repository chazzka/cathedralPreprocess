import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans


import pickle


def doTrain(X_train):
    return ellipticTrain(X_train)


def findCluster(X_Train):
    return findClusterKMeans(X_Train)


def findClusterDBScan(X_train):
    return DBSCAN(eps=0.5, min_samples=10).fit_predict(X_train)


def findClusterKMeans(X_train):
    return KMeans(n_clusters=2, random_state=0, n_init="auto", algorithm="elkan").fit_predict(X_train)

def forestTrain(X_train):
    clf = IsolationForest(max_samples=10, contamination=0.07, random_state=0)
    return clf.fit(X_train)


def svmTrain(X_train):
    return OneClassSVM(gamma='auto', kernel='linear').fit(X_train)


def ellipticTrain(X_train):
    return EllipticEnvelope(random_state=0, assume_centered=True, contamination=0.1).fit(X_train)


def localOutlierTrain(X_train):
    return LocalOutlierFactor(n_neighbors=5, contamination=0.5).fit_predict(X_train)


def saveModel(model):
    filename = 'model.pckl'
    pickle.dump(model, open(f'models/{filename}', 'wb'))


def loadModel(path):
    return pickle.load(open(path, 'rb'))
