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
import pandas

# accept dataframe, return trained model


def train(df: pandas.DataFrame, trainingColumnName: str):
    trainingData = df[[trainingColumnName]]
    labels = ellipticTrain(trainingData)


# accept trained model and dataframe, return dataframe with predicted values
def predict(df: pandas.DataFrame, timeColumnName, averageColumnName, model):
    prediction = model.predict(df[[averageColumnName]])
    predictedDf = df.assign(isAnomaly=prediction)
    return getClusters(predictedDf, timeColumnName, averageColumnName)


def getClusters(df, timeColumnName, averageColumnName):
    anomalies = getAnomalies(df)

    try:
        cluster = findCluster(anomalies[[timeColumnName, averageColumnName]])
    except:
        print("no cluster found")
        return 1
    finally:
        # here might be better to assign to the previous df, not only anomalies
        return anomalies.assign(isCluster=cluster)


def getAnomalies(df):
    return df[(df.isAnomaly == -1)]


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
