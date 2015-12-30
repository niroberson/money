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
        if 'weight' in relationship:
            self.distance = relationship['weight']
            self.update = False
            print('Got weight from database as: %f' % (self.distance) )
        else:
            self.distance = None
            self.update = True


class Graph(nx.MultiDiGraph):
    # Build a networkX graph from concepts and relationships
    def __init__(self, config, dev_flag):
        nx.MultiDiGraph.__init__(self)
        self.database = Database(config, dev_flag)
        self.dev_flag = dev_flag

    def update(self, node=None, edge=None):
        if node:
            self.add_node(node.id, properties=node.properties, ids=node.ids)
            print('Added: %s' % (node.properties['NAME']))
        if edge:
            self.add_edge(edge.source_node.id, edge.target_node.id, key=edge.id, weight=edge.distance, properties=edge.properties)
            print('Added edge: %s:%s:%s to graph network' % (edge.source_node.properties['NAME'], edge.type,
                                                                     edge.target_node.properties['NAME']))
            if self.dev_flag and edge.update:
                self.set_weight(edge)

    def set_weight(self, edge):
        self.database.set_weight(edge)
        print("Set weight in database as %f" % (edge.distance))

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
        [self.update(node=Node(node)) for node in bfs_nodes]

    def load_source_edges(self, source):
        # Get all current graph nodes
        nodes = self.nodes()
        # Get these edges
        edges = self.database.one_to_many_edges(source, nodes)
        edges = [Edge(edgeX) for edgeX in edges]
        edges = self.compute_distances(edges)
        [self.update(edge=edgeX) for edgeX in edges]

    def load_edges_from_graph(self, source_node):
        edges = self.database.bfs_edges(source_node)
        for edgeX in edges:
            for edgeY in edgeX:
                # Determine if this edge is already in the network
                edgeY = Edge(edgeY)
                if self.has_edge(edgeY.source_node.id, edgeY.target_node.id, key=edgeY.id):
                    continue
                elif edgeY.distance is None:
                    edgeY.distance = self.compute_distance(edgeY)
                self.update(edge=edgeY)

    def create_subgraph(self, source_node):
        # Get the sub-graph connected to this node
        self.load_nodes_from_source(source_node)
        self.load_edges_from_graph(source_node)

    def compute_distances(self, edges):
        results = []
        for edge in edges:
            edge.distance = self.compute_distance(edge)
            results.append(edge)
        return results

    def compute_distance(self, edge):
        # TODO: Add COUNT of predication not just number of relationships here
        n_i = [int(edgeX.properties['COUNT']) for edgeX in self.database.one_to_many_edges(edge.source_node)]
        n_i = sum(n_i)
        n_j = [int(edgeX.properties['COUNT']) for edgeX in self.database.one_to_many_edges(edge.target_node)]
        n_j = sum(n_j)
        n_i_j = int(edge.properties['COUNT'])
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = 1/ksp - 1
        return d

    def get_shortest_paths(self, source_node):
        paths = nx.single_source_dijkstra_path(self, source_node.id)
        path_lengths = nx.single_source_dijkstra_path_length(self, source_node.id)
        return paths, path_lengths

    def traverse(self):
        edge_ids = self.database.get_all_edge_ids()
        for eid in edge_ids:
            eid = eid[0]
            edge = self.database.get_edge_by_id(eid)
            edge = Edge(edge)
            if edge.distance is None:
                edge.distance = self.compute_distance(edge)
                self.set_weight(edge)