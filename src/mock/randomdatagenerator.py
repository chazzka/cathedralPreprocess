from sklearn.datasets import make_blobs, make_regression
import numpy as np
from itertools import *


class Result:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def generateRandomClusters(centers, n_samples=100):
    features, Y1 = make_blobs(
        n_samples=n_samples, n_features=2, centers=centers, cluster_std=7)
    return Result(list(features[:, 0]), list(features[:, 1]))


def generateLinearSpace(n_samples=100, ymutator=lambda x: 5*x + 100, leftBoundary=0, rightBoundary=100):
    X_space = list(rightBoundary* np.random.random_sample(n_samples) +leftBoundary)
    Y, labels = make_regression(n_features=1, n_samples=n_samples)
    return Result(list(X_space), list(map(ymutator, Y.flatten())))


def generateRandomData(generators: list[Result]) -> chain:
    return chain.from_iterable(map(lambda res: zip(res.x,res.y), generators))


def createRandomData() -> chain:
    def s(x): return 2*x + 200
    def r(x): return 2*x + 150
    return generateRandomData([
        generateRandomClusters(centers=[(80, 200), (100,200), (20,200)]),
        generateLinearSpace(leftBoundary=50,rightBoundary=100),
        generateLinearSpace(leftBoundary=0,rightBoundary=40),
        #generateLinearSpace(20, s),
        #generateLinearSpace(20, r),
    ])


def combineListsOfStruct(l: list[Result], feature):
    return sum([res.__getattribute__(feature) for res in l], [])
