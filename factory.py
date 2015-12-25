from analysis import Analyzer
from pandas import DataFrame
from database import Database
from graph import Node, Edge, Graph


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, dev_flag):
        self.database = Database(dev_flag)
        self.analyzer = Analyzer()
        self.graph = None

    def search_concept(self, concept):
        # Find the node associated with this concept
        node_of_interest = self.database.get_node_by_name(concept)

        # Get the sub-graph connected to this node
        nodes = self.database.get_direct_nodes(node_of_interest)
        edges = self.database.get_direct_edges(node_of_interest)

        # Compute distances between all concept relationships

        # Create a networkX graph based on this node
        self.graph = Graph(nodes, edges)
        # Get a dictionary of the shortest paths based on this node
        self.graph.get_shortest_paths(node_of_interest)

        # Return a table sorted by shortest path lengths