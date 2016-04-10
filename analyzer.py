from database import Database
from graph import Node
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame


class Analyzer(object):
    def __init__(self, config):
        self.database = Database(config)

    def subgraph_distribution(self, targets):
        counts = [self.database.count_one_to_many_nodes(target) for target in targets]
        plt.hist(counts)
        plt.show()

    def calculate_features(self, source, targets):
        cn = np.array([self.common_neighbors(source, target) for target in targets])
        jc = np.array([self.jaccards_coefficient(source, target) for target in targets])
        ad = np.array([self.adamic(source, target) for target in targets])
        pa = np.array([self.preferential_attachment(source, target) for target in targets])
        features = np.array((cn, jc, ad, pa))
        features = DataFrame(features.T)
        index = [target.id for target in targets]
        return features, index

    def common_neighbors(self, source, target):
        nodes1 = self.database.one_to_many_nodes(source)
        nodes2 = self.database.one_to_many_nodes(target)
        n1 = set([Node(n).id for n in nodes1])
        n2 = set([Node(n).id for n in nodes2])
        score = len(n1.intersection(n2))
        return score

    def jaccards_coefficient(self, source,target):
        nodes1 = self.database.one_to_many_nodes(source)
        nodes2 = self.database.one_to_many_nodes(target)
        n1 = set([Node(n).id for n in nodes1])
        n2 = set([Node(n).id for n in nodes2])
        score = len(n1.intersection(n2)) / len(n1.union(n2))
        return score

    def adamic(self, source, target):
        nodes1 = self.database.one_to_many_nodes(source)
        nodes2 = self.database.one_to_many_nodes(target)
        n1 = set([Node(n).id for n in nodes1])
        n2 = set([Node(n).id for n in nodes2])
        n3 = n1.intersection(n2)
        score = sum([1 / np.log(len(self.database.one_to_many_nodes(Node(self.database.get_edge_by_id(n))))) for n in n3])
        return score

    def preferential_attachment(self, source, target):
        nodes1 = self.database.one_to_many_nodes(source)
        nodes2 = self.database.one_to_many_nodes(target)
        n1 = set([Node(n).id for n in nodes1])
        n2 = set([Node(n).id for n in nodes2])
        score = len(n1) * len(n2)
        return score

    def ksp(self, source, target):
        n_i = self.database.sum_count_one_to_many_edges(source)
        n_j = self.database.sum_count_one_to_many_edges(target)
        # Get shortest path between nodes here
        n_i_j = int(source['COUNT'])
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = 1/ksp - 1
        return d

