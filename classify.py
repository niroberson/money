from pandas import DataFrame
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


class Classify(object):

    def __init__(self, database):
        self.database = database
        self.features = DataFrame.from_csv('features.csv')

    def cluster(self):
        estimator = KMeans(n_clusters=2)
        estimator.fit(self.features)
        fig = plt.figure(1, figsize=(4, 3))
        ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
        labels = estimator.labels_
        ax.scatter(self.features[:, 3], self.features[:, 0], self.features[:, 2], c=labels.astype(np.float))

if __name__ == "__main__":
    c = Classify()
    c.cluster()
