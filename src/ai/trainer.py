import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

import pickle


def doTrain(X_train):
    clf = IsolationForest(max_samples=10, contamination=0.07, random_state=0)
    return clf.fit(X_train)


def saveModel(model):
    filename = 'model.pckl' 
    pickle.dump(model, open(f'models/{filename}', 'wb'))


def loadModel(path):
    return pickle.load(open(path, 'rb'))