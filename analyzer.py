from database import Database
from config import Config
from graph import Node
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame


class Analyzer(object):
    def __init__(self):
        self.database = Database(Config(False))

    def get_subgraph_nodes(self, source):
        nodes = self.database.bfs_nodes(source, max_level=2)
        return nodes

    def subgraph_distribution(self, targets):
        counts = [self.database.count_one_to_many_nodes(target) for target in targets]
        plt.hist(counts)
        plt.show()

    def calculate_features(self, source, targets):
        cn = np.array([a.common_neighbors(source, target) for target in targets])
        jc = np.array([a.jaccards_coefficient(source, target) for target in targets])
        ad = np.array([a.adamic(source, target) for target in targets])
        pa = np.array([a.preferential_attachment(source, target) for target in targets])
        features = np.array((cn, jc, ad, pa))
        features = DataFrame(features.T)
        index = [target.id for target in targets]
        features.to_csv('features.csv', index=index)

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


if __name__ == "__main__":
    a = Analyzer()
    source = Node(a.database.get_node_by_name('BRCA1'))
    targets = a.get_subgraph_nodes(source)
    targets = [Node(target) for target in targets]
    a.calculate_features(source, targets)
    #a.subgraph_distribution(targets)


