from database import Database
from graph import Graph
from results import Results


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, dev_flag):
        self.graph = Graph(dev_flag)

    def search_concept(self, concept):

        # Get a dictionary of the shortest paths based on this node
        paths = self.graph.get_shortest_paths(node_of_interest)

        # Return a table sorted by shortest path lengths
        Results(nodes, edges, paths)


