from database import Database
from graph import Graph
from results import Results


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, dev_flag):
        self.database = Database(dev_flag)
        self.graph = None

    def search_concept(self, concept):
        # Find the node associated with this concept
        node_of_interest = self.database.get_node_by_name(concept)

        # Get the sub-graph connected to this node

        # Get BFS level 1
        # nodes, edges = self.database.bfs_from_node(node_of_interest, 2)
        nodes = self.database.get_direct_nodes(node_of_interest)
        edges = self.database.get_direct_edges(node_of_interest)

        for nodeX in nodes:
            nodes.update(self.database.get_direct_nodes(nodeX))
            edges.update(self.database.get_direct_edges(nodeX))

        # Compute distances between all concept relationships
        for edgeX in edges:
            if hasattr(edgeX.properties, 'score'):
                edgeX.distance = edgeX.properties.score
            else:
                edgeX.distance = self.compute_distance(edgeX.source_node, edgeX.target_node)

        # Create a networkX graph based on this node
        self.graph = Graph(nodes, edges)
        # Get a dictionary of the shortest paths based on this node
        paths = self.graph.get_shortest_paths(node_of_interest)

        # Return a table sorted by shortest path lengths
        print(paths)
        Results(nodes, edges, paths)

    def compute_distance(self, node_source, node_target):
        n_i = self.database.get_count_direct_edges(node_source)
        n_j = self.database.get_count_direct_edges(node_target)
        n_i_j = self.database.get_count_between_nodes(node_source, node_target)
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = 1/ksp - 1
        return d
