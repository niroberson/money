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
            print('Added %s to graph network\n' % (node.properties['NAME']))
        if edge:
            self.add_edge(edge.source_node.id, edge.target_node.id, weight=edge.distance, properties=edge.properties)
            print('Added edge between %s and %s to graph network\n' % (edge.source_node.properties['NAME'],
                                                                     edge.target_node.properties['NAME']))

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

    def create_subgraph(self, source_node):

        # nodes = self.database.bfs_nodes(source_node)
        # nodes = [Node(nodeX) for nodeX in nodes]
        # [self.update(node=nodeX) for nodeX in nodes]

        # Get the sub-graph connected to this node
        nodes = self.database.one_to_many_nodes(source_node)
        nodes = [Node(nodeX) for nodeX in nodes]
        [self.update(node=nodeX) for nodeX in nodes]

        # Get all indirect nodes for each direct node
        for nodeX in nodes:
            nodesX = [self.database.one_to_many_nodes(nodeX)]
            nodesX = [Node(nodeY) for nodeY in nodesX]
            [self.update(node=nodeY) for nodeY in nodesX]

            # Compute distances between all concept relationships
            edges = [self.database.one_to_one_edges(nodeX, nodeY) for nodeY in nodes]
            for edgeX in edges:
                for edgeY in edgeX:
                    edgeY = Edge(edgeY)
                    edgeY.distance = self.compute_distance(edgeY.source_node, edgeY.target_node)
                    self.update(edge=edgeY)

    def compute_distance(self, node_source, node_target):
        n_i = self.database.count_one_to_many_edges(node_source)
        n_j = self.database.count_one_to_many_edges(node_target)
        n_i_j = self.database.count_one_to_one_edges(node_source, node_target)
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = 1/ksp - 1
        return d

    def get_shortest_paths(self, source_node):
        paths = nx.single_source_dijkstra_path(self, source_node.id)
        path_lengths = nx.single_source_dijkstra_path_length(self, source_node.id)
        return paths, path_lengths
