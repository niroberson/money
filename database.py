from py2neo import Graph
from py2neo.packages.httpstream import http


class Database:
    def __init__(self, config, dev_flag=True):
        self.config = config
        self.dev_flag = dev_flag
        self.connection = self.connect()
        http.socket_timeout = 9999

    def connect(self):
        if self.dev_flag:
            return self.connect_local()
        else:
            return self.connect_local()
            # TODO: return self.connect_production()

    def connect_local(self):
        endpoint = Database.create_endpoint(self.config.host_local, self.config.user, self.config.pw)
        return Graph(endpoint)

    @staticmethod
    def create_endpoint(host, user, password):
        return "http://" + user + ":" + password + "@" + host

    def execute_query(self, cypher_query, limit=None):
        if self.dev_flag and limit:
            cypher_query += " LIMIT " + str(limit)
        return self.connection.cypher.execute(cypher_query)

    def get_node_by_name(self, search_input):
        cypher_query = "MATCH (a:Concept { NAME:'" + search_input + "'}) RETURN a"
        node = self.execute_query(cypher_query)
        return node.one

    def get_node_by_id(self, id):
        cypher_query = "MATCH (a) WHERE id(a)=" + id + " RETURN a"
        node = self.execute_query(cypher_query)
        return node.one

    def get_all_node_ids(self):
        cypher_query = "MATCH (a:Concept) RETURN id(a)"
        return self.execute_query(cypher_query)

    def one_to_many_nodes(self, node):
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + str(node.id) + " RETURN b"
        node_store = []
        for nodeX in self.execute_query(cypher_query, 10):
            node_store.append(nodeX.b)
        return node_store

    def one_to_one_edges(self, node1, node2):
        # Not necessarily one edge between nodes can't take [0] need to specify rel label
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + str(node1.id) + " AND id(b)=" + str(node2.id) + " RETURN r"
        edge_store = []
        for edgeX in self.execute_query(cypher_query):
            edge_store.append(edgeX.r)
        return edge_store

    def one_to_many_edges(self, source=None, id=None, targets=None, exclude=None):
        source_id = None
        if source:
            source_id = str(source.id)
        elif id:
            source_id = str(id)
        if targets:
            cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + source_id + " AND id(b) IN " + str(targets) + " RETURN r"
        elif exclude:
            cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + source_id + " AND NOT id(b)=" + str(exclude.id) + " RETURN r"
        else:
            cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + source_id + " RETURN r"
        edge_store = []
        for edgeX in self.execute_query(cypher_query):
            edge_store.append(edgeX.r)
        return edge_store

    def count_one_to_many_edges(self, node):
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + str(node.id) + " RETURN count(r)"
        count = self.execute_query(cypher_query)
        return count.one

    def count_one_to_many_nodes(self, node):
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + str(node.id) + " RETURN count(b)"
        count = self.execute_query(cypher_query)
        return count.one

    def count_one_to_one_edges(self, node1, node2):
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + str(node1.id) + " AND id(b)=" + str(node2.id) + " RETURN count(r)"
        count = self.execute_query(cypher_query)
        return count.one

    def bfs_nodes(self, source_node=None, id=None):
        if source_node:
            cypher_query = "START n=node(" + str(source_node.id) + ") MATCH (n)-[r*0..2]->(b) WHERE NOT id(b)=" + str(source_node.id) + " RETURN b"
        else:
            cypher_query = "START n=node(" + str(id) + ") MATCH (n)-[r*0..2]->(b) WHERE NOT id(b)=" + str(id) + " RETURN b"
        node_store = []
        for nodeX in self.execute_query(cypher_query, 100):
            node_store.append(nodeX.b)
        return node_store

    def bfs_edges(self, source_node):
        cypher_query = "START n=node(" + str(source_node.id) + ") MATCH (n)-[r*0..2]->(b) WHERE NOT id(b)=" + str(source_node.id) + " RETURN r"
        edge_store = []
        for edgeX in self.execute_query(cypher_query, 100):
            edge_store.append(edgeX.r)
        return edge_store

    def set_weight(self, edge):
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(r)=" + str(edge.id) + " SET r.weight=" + str(edge.distance) + " RETURN r"
        return self.execute_query(cypher_query)
