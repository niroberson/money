from py2neo import Graph

class Database:
    def __init__(self, dev_flag=True):
        self.user = "neo4j"
        self.password = "newk1ng$!"
        self.host_local = "localhost:7474/db/data"
        self.connection = self.connect_local()
        self.dev_flag = dev_flag

    def connect_local(self):
        endpoint = Database.create_endpoint(self.host_local, self.user, self.password)
        return Graph(endpoint)

    @staticmethod
    def create_endpoint(host, user, password):
        return "http://" + user + ":" + password + "@" + host

    def execute_query(self, cypher_query):
        if self.dev_flag:
            cypher_query += " LIMIT 100"
        return self.connection.cypher.execute(cypher_query)

    def get_node_by_name(self, search_input):
        cypher_query = "MATCH (a:Concept { NAME:'" + search_input + "'}) RETURN a"
        node = self.execute_query(cypher_query)
        return node.one

    def get_node_by_id(self, id):
        cypher_query = "MATCH (a) WHERE id(a)=" + id + " RETURN a"
        node = self.execute_query(cypher_query)
        return node.one

    def get_direct_edges(self, node):
        cypher_query = "MATCH (a)-[r]-b WHERE id(a)=" + str(node.id) + " RETURN r"
        edge_store = []
        for edgeX in self.execute_query(cypher_query):
            edge_store.append(edgeX.r)
        return edge_store

    def get_direct_nodes(self, node):
        """
        :param node: A single node of interest for which to get all nodes directly attached to it
        :param graph: A graph storage for which to place the results of the query
        :return: Graph with query results inside of it
        """
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + str(node.id) + " RETURN b"
        node_store = []
        for nodeX in self.execute_query(cypher_query):
            node_store.append(nodeX.b)
        return node_store

    def get_edges_between_two_nodes(self, node1, node2):
        # Not necessarily one edge between nodes can't take [0] need to specify rel label
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + node1.id + " AND id(b)=" + node2.id + " RETURN r"
        return self.execute_query(cypher_query)

    def get_edges_between_many_nodes(self, nodes):
        nodes_id = [node.id for node in nodes]
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a) IN " + nodes_id + " AND id(b) IN " + nodes_id + " RETURN r"
        return self.execute_query(cypher_query)

    def get_count_direct_edges(self, node):
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + str(node.id) + " RETURN count(r)"
        count = self.connection.cypher.execute(cypher_query)
        return count.one

    def get_count_direct_nodes(self, node):
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + str(node.id) + " RETURN count(b)"
        count = self.connection.cypher.execute(cypher_query)
        return count.one

    def get_count_between_nodes(self, node1, node2):
        cypher_query = "MATCH (a)-[r]-(b) WHERE id(a)=" + str(node1.id) + " AND id(b)=" + str(node2.id) + " RETURN count(r)"
        count = self.connection.cypher.execute(cypher_query)
        return count.one