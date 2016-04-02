from database import Database
from config import Config
from graph import Node, Edge, Graph


class Analyzer(object):
    def __init__(self):
        self.database = Database(Config(True))

    def get_subgraph_nodes(self, source):
        source_node = Node(self.database.get_node_by_name(source))
        nodes = self.database.bfs_nodes(source_node, max_level=2)
        return nodes

    def PageRank(self, source, target):
        pass

    def CommonNeighbors(self, source, target):
        pass

    def KSP(self, source, target):
        n_i = self.get_node_count(source)
        n_j = self.get_node_count(target)
        n_i_j = int(self.properties['COUNT'])
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = 1/ksp - 1
        return d


if __name__ == "__main__":
    a = Analyzer()
    a.get_subgraph_nodes('BRCA1')