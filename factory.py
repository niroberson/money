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

        # Get the subgraph connected to this node
        nodes = self.database.get_direct_nodes(node_of_interest)
        edges = self.database.get_direct_edges(node_of_interest)

        # Compute distances between all concept relationships

        # Create a networkX graph based on this node
        self.graph = Graph(nodes, edges)
        # Get a dictionary of the shortest paths based on this node
        self.graph.get_shortest_paths(node_of_interest)


    def compute_distances_single_source_node(self, node_of_interest):
        n_i = self.get_num_rels(node_of_interest)
        direct_nodes = self.database.get_direct_nodes(node_of_interest)
        df = DataFrame()
        for node in direct_nodes:
            dx = self.compute_distance(node_of_interest, node, n_i)
            dfx = DataFrame([[node_of_interest.properties['NAME'], node_of_interest.properties['CUI'],
                              node[0].properties['NAME'], node[0].properties['CUI'], dx]],
                            columns=['source_name', 'source_id', 'target_name', 'target_id', 'distance'])
            df = df.append(dfx)
        return df
