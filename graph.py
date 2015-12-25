import networkx as nx


class Node:
    def __init__(self, node):
        self.id = node._id
        self.properties = node.properties


class Edge:
    def __init__(self, relationship):
        self.id = relationship._id
        self.type = relationship.type
        self.properties = relationship.properties
        self.source_node = Node(relationship.start_node)
        self.target_node = Node(relationship.end_node)
        self.distance = None


class Graph:
    # Build a networkX graph from concepts and relationships
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.graph = None

    def create_graph(self):
        # Create list of nodes digestible by NetworkX
        node_list = []
        for node in self.nodes:
            node_list.append(node.id)

        # Create list of edges digestible by NetworkX
        edge_list = []
        for edge in self.edges:
            edge_list.append((edge.source_node.id, edge.target_node.id, edge.distance))

        # Create the networkX graph from these lists
        self.graph = nx.MultiDiGraph()
        self.graph.add_nodes_from(node_list)
        self.graph.add_weighted_edges_from(edge_list)



