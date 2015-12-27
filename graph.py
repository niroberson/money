import networkx as nx
from database import Database


class GraphObject:
    def __init__(self, obj):
        self.id = obj._id
        self.properties = obj.properties


class Node(GraphObject):
    def __init__(self, node):
        GraphObject.__init__(self, node)


class Edge(GraphObject):
    def __init__(self, relationship):
        GraphObject.__init__(self, relationship)
        self.type = relationship.type
        self.source_node = Node(relationship.start_node)
        self.target_node = Node(relationship.end_node)
        self.distance = None


class Graph(nx.MultiDiGraph):
    # Build a networkX graph from concepts and relationships
    def __init__(self, dev_flag):
        nx.MultiDiGraph.__init__(self)
        self.database = Database(dev_flag)

    def update(self, node=None, edge=None):
        if node:
            self.add_node(node.id, properties=node.properties)
        if edge:
            self.add_edge(edge.source_node.id, edge.target_node.id, weight=edge.distance, properties=edge.properties)

    def update_from(self, nodes=None, edges=None):
        """
        Method to update graph from given nodes and edges
        :return:
        """
        # Add nodes into graph
        for node in nodes:
            self.add_node(node.id, properties=node.properties)  # Add attributes of Node to network

        # Add edges into graph
        for edge in edges:
            self.add_edge(edge.source_node.id, edge.target_node.id, weight=edge.distance, properties=edge.properties)
            # Add all attributes of Edge to network

    def get_node_by_name(self, name):
        this_node = Node(self.database.get_node_by_name(name))
        self.update(this_node)
        return this_node

    def create_subgraph_from_source(self, source_node):

        # Get the sub-graph connected to this node
        nodes = self.database.get_direct_nodes(source_node)
        for nodeX in nodes:
            nodeX = Node(nodeX)
            # Add node to network
            self.update(node=nodeX)
            # Get direct nodes of this node
            indirect_nodes = self.database.get_direct_nodes(nodeX)
            for nodeY in indirect_nodes:
                nodeY = Node(nodeY)
                self.update(node=nodeY)

        # Get all edges between found nodes
        edges = self.database.get_edges_between_many_nodes(self.nodes())

        # Compute distances between all concept relationships
        for edgeX in edges:
            edgeX = Edge(edgeX)
            if hasattr(edgeX.properties, 'score'):
                edgeX.distance = edgeX.properties.score
            else:
                edgeX.distance = self.compute_distance(edgeX.source_node, edgeX.target_node)
            # Add edge to network
            self.update(edge=edgeX)

    def compute_distance(self, node_source, node_target):
        n_i = self.database.get_count_direct_edges(node_source)
        n_j = self.database.get_count_direct_edges(node_target)
        n_i_j = self.database.get_count_between_nodes(node_source, node_target)
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = 1/ksp - 1
        return d

    def get_shortest_paths(self, source_node):
        return nx.single_source_dijkstra_path_length(self, source_node.id)
