import networkx as nx
from database import Database


class GraphObject(object):
    def __init__(self, obj):
        if hasattr(obj, '_id'):
            self.id = obj._id
        if hasattr(obj, 'properties'):
            self.properties = obj.properties


class Node(GraphObject):
    def __init__(self, node=None, id=None, prop=None, database=None):
        GraphObject.__init__(self, node)
        if id:
            self.id = str(id)
        if prop:
            self.properties = prop
        if database:
            self.database = database

        if hasattr(node, 'count'):
            self.count = node['count']
        elif database:
            self.count = self.compute_count()
            self.set_count()

    def compute_count(self):
        n_i = self.database.sum_count_one_to_many_edges(self)
        return n_i

    def set_count(self):
        self.database.set_count(self)


class Edge(GraphObject):
    def __init__(self, relationship, database):
        GraphObject.__init__(self, relationship)
        self.database = database
        self.type = relationship.type
        self.source_node = Node(relationship.start_node, database=self.database)
        self.target_node = Node(relationship.end_node, database=self.database)
        if 'weight' in relationship:
            self.distance = relationship['weight']
        else:
            self.distance = self.compute_distance()
            self.set_weight()

    def compute_distance(self):
        n_i = self.get_node_count(self.source_node)
        n_j = self.get_node_count(self.target_node)
        n_i_j = int(self.properties['COUNT'])
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = 1/ksp - 1
        return d

    def get_node_count(self, node):
        if hasattr(node, 'count'):
            return node.count
        else:
            n = self.database.sum_count_one_to_many_edges(self.source_node)
            self.source_node.count = n
            self.source_node.set_count()
            return n

    def set_weight(self):
        self.database.set_weight(self)


class Graph(nx.MultiDiGraph):
    # Build a networkX graph from concepts and relationships
    def __init__(self, config):
        nx.MultiDiGraph.__init__(self)
        self.database = Database(config)
        self.config = config

    def update(self, node=None, edge=None):
        if node:
            self.add_node(node.id, properties=node.properties)
        if edge:
            self.add_edge(edge.source_node.id, edge.target_node.id, key=edge.id, weight=edge.distance,
                          properties=edge.properties, type=edge.type)

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
        this_node = Node(self.database.get_node_by_name(name), database=self.database)
        self.update(this_node)
        return this_node

    def get_local_node_by_id(self, id):
        node = self.node[id]
        node['id'] = id
        return Node(id=id, prop=node['properties'])

    def load_nodes_from_source(self, source, max_level):
        bfs_nodes = self.database.bfs_nodes(source, max_level=max_level)
        [self.update(node=Node(node, database=self.database)) for node in bfs_nodes]

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

    def connect_two_nodes(self, node1, node2):
        edges = self.database.one_to_one_edges(node1, node2, max_level=2)
        for edgeX in edges:
            for edgeY in edgeX:
                edgeY = Edge(edgeY, self.database)
                self.update(edge=edgeY)
                self.update(node=edgeY.source_node)
                self.update(node=edgeY.target_node)

    def get_shortest_paths(self, source_node, target_node=None):
        if target_node:
            path_lengths, paths = nx.single_source_dijkstra(self, source_node.id, target_node.id)
        else:
            paths = nx.single_source_dijkstra_path(self, source_node.id)
            path_lengths = nx.single_source_dijkstra_path_length(self, source_node.id)
        return paths, path_lengths

    def create_edge(self, eid):
        Edge(self.database.get_edge_by_id(eid), self.database)

    def create_node(self, nid):
        Node(node=self.database.get_node_by_id(nid), database=self.database)
