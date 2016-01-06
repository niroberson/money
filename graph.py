from numba import autojit
import networkx as nx
from database import Database


class GraphObject(object):
    def __init__(self, obj):
        if hasattr(obj, '_id'):
            self.id = obj._id
        if hasattr(obj, 'properties'):
            self.properties = obj.properties


class Node(GraphObject):
    def __init__(self, node=None, id=None, prop=None):
        GraphObject.__init__(self, node)
        if id:
            self.id = str(id)
        if prop:
            self.properties = prop


class Edge(GraphObject):
    def __init__(self, relationship, database):
        GraphObject.__init__(self, relationship)
        self.database = database
        self.type = relationship.type
        self.source_node = Node(relationship.start_node)
        self.target_node = Node(relationship.end_node)
        if 'weight' in relationship:
            self.distance = relationship['weight']
            print('Got Edge: %s:%s:%s Weight:%f' % (self.source_node.properties['NAME'], self.type,
                                                    self.target_node.properties['NAME'], self.distance))
        else:
            self.distance = self.compute_distance()
            self.set_weight()

    def compute_distance(self):
        n_i = self.database.sum_count_one_to_many_edges(self.id, self.source_node)
        n_j = self.database.sum_count_one_to_many_edges(self.id, self.target_node)
        n_i_j = int(self.properties['COUNT'])
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = 1/ksp - 1
        return d

    def set_weight(self):
        self.database.set_weight(self)
        print('Set Edge: %s:%s:%s Weight:%f' % (self.source_node.properties['NAME'], self.type,
                                                self.target_node.properties['NAME'], self.distance))


class Graph(nx.MultiDiGraph):
    # Build a networkX graph from concepts and relationships
    def __init__(self, config):
        nx.MultiDiGraph.__init__(self)
        self.database = Database(config)
        self.config = config

    def update(self, node=None, edge=None):
        if node:
            self.add_node(node.id, properties=node.properties)
            print('Added: %s' % (node.properties['NAME']))
        if edge:
            self.add_edge(edge.source_node.id, edge.target_node.id, key=edge.id, weight=edge.distance,
                          properties=edge.properties, type=edge.type)
            print('Added edge: %s:%s:%s to network' % (edge.source_node.properties['NAME'], edge.type,
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

    def load_nodes_from_source(self, source, max_level):
        bfs_nodes = self.database.bfs_nodes(source, max_level=max_level)
        [self.update(node=Node(node)) for node in bfs_nodes]

    def load_source_edges(self, source):
        # Get all current graph nodes
        nodes = self.nodes()
        # Get these edges
        edges = self.database.one_to_many_edges(source, nodes)
        edges = [Edge(edgeX, self.database) for edgeX in edges]
        [self.update(edge=edgeX) for edgeX in edges]

    def load_edges_from_graph(self, source_node, predication, max_level):
        edges = self.database.bfs_edges(source_node, predication=predication, max_level=max_level)
        count = 0
        fin = len(edges)
        for edgeX in edges:
            print('Loading relationship %i of %i' % (count, fin))
            count += 1
            for edgeY in edgeX:
                # Determine if this edge is already in the network
                if self.has_edge(edgeY.start_node._id, edgeY.end_node._id, key=edgeY._id):
                    continue
                edgeY = Edge(edgeY, self.database)
                self.update(edge=edgeY)

    def create_subgraph(self, source_node, predication=None, max_level=1):
        # Get the sub-graph connected to this node
        self.load_nodes_from_source(source_node, max_level=max_level)
        self.load_edges_from_graph(source_node, predication=predication, max_level=max_level)

    def get_shortest_paths(self, source_node):
        paths = nx.single_source_dijkstra_path(self, source_node.id)
        path_lengths = nx.single_source_dijkstra_path_length(self, source_node.id)
        return paths, path_lengths

    @autojit
    def create_edge(self, eid):
        Edge(self.database.get_edge_by_id(eid), self.database)
