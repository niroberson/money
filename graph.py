import networkx as nx
from database import Database


class GraphObject:
    def __init__(self, obj):
        if hasattr(obj, '_id'):
            self.id = obj._id
            self.ids = str(obj._id)
        if hasattr(obj, 'properties'):
            self.properties = obj.properties


class Node(GraphObject):
    def __init__(self, node=None, id=None, prop=None):
        GraphObject.__init__(self, node)
        if id:
            self.id = id
            self.ids = str(id)
        if prop:
            self.properties = prop


class Edge(GraphObject):
    def __init__(self, relationship):
        GraphObject.__init__(self, relationship)
        self.type = relationship.type
        self.source_node = Node(relationship.start_node)
        self.target_node = Node(relationship.end_node)
        self.distance = None


class Graph(nx.MultiDiGraph):
    # Build a networkX graph from concepts and relationships
    def __init__(self, config, dev_flag):
        nx.MultiDiGraph.__init__(self)
        self.database = Database(dev_flag, config)

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

    def get_local_node_by_id(self, id):
        node = self.node[id]
        node['id'] = id
        return Node(id=id, prop=node['properties'])

    def load_graph_from_source(self, source):
        # Get directly associated nodes
        nodes = self.database.one_to_many_nodes(source)
        nodes = [Node(nodeX) for nodeX in nodes]
        [self.update(node=nodeX) for nodeX in nodes]

        # Get these edges
        node_ids = [nodeX.id for nodeX in nodes]
        edges = self.database.one_to_many_edges(source, node_ids)
        edges = [Edge(edgeX) for edgeX in edges]
        edges = self.compute_distances(edges)
        [self.update(edge=edgeX) for edgeX in edges]

    def create_subgraph(self, source_node):

        # nodes = self.database.bfs_nodes(source_node)
        # nodes = [Node(nodeX) for nodeX in nodes]
        # [self.update(node=nodeX) for nodeX in nodes]

        # Get the sub-graph connected to this node
        self.load_graph_from_source(source_node)

        # For each node now in the graph, do the same thing
        current_nodes = self.nodes()
        current_nodes = [self.get_local_node_by_id(nodeX_id) for nodeX_id in current_nodes]
        [self.load_graph_from_source(nodeX) for nodeX in current_nodes]

    def compute_distances(self, edges):
        results = []
        for edge in edges:
            edge.distance = self.compute_distance(edge.source_node, edge.target_node)
            results.append(edge)
        return results

    def compute_distance(self, node_source, node_target):
        # TODO: Add count of relationship not just number of relationships here
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
