from database import Database
from config import Config
from graph import Node, Edge, Graph


class Analyzer(object):
    def __init__(self):
        self.database = Database(Config(False))

    def get_subgraph_nodes(self, source):
        nodes = self.database.bfs_nodes(source, max_level=2)
        return nodes

    def commonNeighbors(self, source, target):
        nodes1 = self.database.one_to_many_nodes(source)
        nodes2 = self.database.one_to_many_nodes(target)

        n1 = set([Node(n).id for n in nodes1])
        n2 = set([Node(n).id for n in nodes2])
        score = len(n1.intersection(n2))
        return score

if __name__ == "__main__":
    a = Analyzer()
    source = Node(a.database.get_node_by_name('BRCA1'))
    targets = a.get_subgraph_nodes(source)
    for target in targets:
        print(a.commonNeighbors(source, Node(target)))