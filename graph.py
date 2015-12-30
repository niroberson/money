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
        self.database = Database(config, dev_flag)

    def update(self, node=None, edge=None):
        if node:
            self.add_node(node.id, properties=node.properties, ids=node.ids)
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
            self.add_node(node.id, properties=node.properties, ids=node.ids)  # Add attributes of Node to network

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

    def load_nodes_from_source(self, source):
        bfs_nodes = self.database.bfs_nodes(source)
        [self.update(Node(node)) for node in bfs_nodes]

    def load_source_edges(self, source):
        # Get all current graph nodes
        nodes = self.nodes()
        # Get these edges
        edges = self.database.one_to_many_edges(source, nodes)
        edges = [Edge(edgeX) for edgeX in edges]
        edges = self.compute_distances(edges)
        [self.update(edge=edgeX) for edgeX in edges]

    def load_graph_edges(self):
        node_ids = self.nodes()
        # Load edges for all nodes
        for node in node_ids:
            this_edges = self.database.one_to_many_edges(id=node, targets=node_ids)
            this_edges = [Edge(edgeX) for edgeX in this_edges]
            this_edges = self.compute_distances(this_edges)
            [self.update(edge=edgeX) for edgeX in this_edges]

    def create_subgraph(self, source_node):
        # Get the sub-graph connected to this node
        self.load_nodes_from_source(source_node)
        self.load_graph_edges()

    def compute_distances(self, edges):
        results = []
        for edge in edges:
            edge.distance = self.compute_distance(edge)
            results.append(edge)
        return results

    def compute_distance(self, edge):
        # TODO: Add count of relationship not just number of relationships here
        n_i = self.database.count_one_to_many_edges(edge.source_node)
        n_j = self.database.count_one_to_many_edges(edge.target_node)
        n_i_j = int(edge.properties['COUNT'])
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = 1/ksp - 1
        return d

    def get_shortest_paths(self, source_node):
        paths = nx.single_source_dijkstra_path(self, source_node.id)
        path_lengths = nx.single_source_dijkstra_path_length(self, source_node.id)
        return paths, path_lengths
