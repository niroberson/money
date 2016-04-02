from database import Database
from config import Config
from graph import Node
import numpy as np


class Analyzer(object):
    def __init__(self):
        self.database = Database(Config(True))
        self.features = None

    def get_subgraph_nodes(self, source):
        nodes = self.database.bfs_nodes(source, max_level=2)
        return nodes

    def calculate_features(self, targets):
        cn = [a.common_neighbors(source, Node(target)) for target in targets]
        jc = [a.jaccards_coefficient(source, Node(target)) for target in targets]
        self.features = [cn, jc]

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
        score = sum([1 / np.log(len(self.database.))])

if __name__ == "__main__":
    a = Analyzer()
    source = Node(a.database.get_node_by_name('BRCA1'))
    targets = a.get_subgraph_nodes(source)
    a.calculate_features(targets)
    pass
