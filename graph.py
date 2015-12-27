import networkx as nx


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
    def __init__(self):
        nx.MultiDiGraph.__init__(self)

    def update_graph(self, nodes=None, edges=None):
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

    def get_shortest_paths(self, source_node):
        return nx.single_source_dijkstra_path_length(self.graph, source_node.id)

    def get_node_from_id(self, id):
        """
        Get a node from the NetworkX graph by its id
        :param id:
        :return:
        """
        pass