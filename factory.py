from pandas import DataFrame
from database import Database
from graph import Node, Edge, Graph


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, dev_flag):
        self.database = Database(dev_flag)
        self.graph = None

    def search_concept(self, concept):
        # Find the node associated with this concept
        node_of_interest = self.database.get_node_by_name(concept)

        # Get the sub-graph connected to this node
        nodes = self.database.get_direct_nodes(node_of_interest)
        edges = self.database.get_direct_edges(node_of_interest)

        # Compute distances between all concept relationships
        for edgeX in edges:
            if edgeX.properties.score:
                edgeX.distance = edgeX.properties.score
            else:
                edgeX.distance = self.compute_distance(edgeX.source_node, edgeX.target_node)
        
        # Create a networkX graph based on this node
        self.graph = Graph(nodes, edges)
        # Get a dictionary of the shortest paths based on this node
        self.graph.get_shortest_paths(node_of_interest)

        # Return a table sorted by shortest path lengths

    def compute_distance(self, node_source, node_target):
        print('Calculating distance between %s and %s' % (node_source.properties['NAME'], node_target[0].properties['NAME']))
        n_i = self.database.get_count_direct_edges(node_source)
        n_j = self.database.get_count_direct_edges(node_target)
        n_i_j = self.database.get_count_between_nodes(node_source, node_target)
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = ([1/ksp - 1])
        return d
