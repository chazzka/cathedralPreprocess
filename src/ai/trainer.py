import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.linear_model import SGDOneClassSVM


import pickle
import pandas
import logging



# accept trained model and dataframe, return dataframe with predicted values
def predict(df: pandas.DataFrame, timeColumnName, averageColumnName, model, aiArgs):
    # without feature names
    prediction = model.predict(df[[timeColumnName, averageColumnName]].values.tolist())

    predictedDf = df.assign(isAnomaly=prediction)
    
    return getClusters(predictedDf, timeColumnName, averageColumnName, aiArgs)


def getClusters(df, timeColumnName, averageColumnName, aiArgs):
    anomalies = getAnomalies(df)
    nonAnomalies = getNonAnomalies(df)

    try:
        cluster = findCluster(anomalies[[timeColumnName, averageColumnName]], aiArgs)
        allClustersTogether = [0 if c>=0 else 1 for c in cluster]
        return pandas.concat([anomalies.assign(isCluster=allClustersTogether), nonAnomalies.assign(isCluster=1)])
    except:
        logging.error("no cluster found")

    # if no cluster found, return all as OK
    return pandas.concat([anomalies.assign(isCluster=1), nonAnomalies.assign(isCluster=1)])



def getAnomalies(df):
    return df[(df.isAnomaly == -1)]


def getNonAnomalies(df):
    return df[(df.isAnomaly == 1)]


def doTrain(X_train, aiArgs):
    return forestTrain(X_train, aiArgs["contamination"])

# 1 - not a cluster
# 0 - is a cluster
def findCluster(X_Train, aiArgs):
    return findClusterDBScan(X_Train, aiArgs["eps"], aiArgs["min_samples"])


def findClusterDBScan(X_train, eps=7, min_samples=10):
    return DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X_train)


def findClusterKMeans(X_train):
    return KMeans(n_clusters=2, random_state=0, n_init="auto", algorithm="lloyd").fit_predict(X_train)


def forestTrain(X_train, contamination=0.02):
    clf = IsolationForest(max_samples='auto', random_state=0, contamination=contamination)
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
