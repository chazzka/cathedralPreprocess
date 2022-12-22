import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest



def doTrain(X_train):
    clf = IsolationForest(max_samples=10, contamination=0.1, random_state=0)
    return clf.fit_predict(X_train)
