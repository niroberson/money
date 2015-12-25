from py2neo import Graph


class Database:
    def __init__(self, dev_flag):
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
            cypher_query += " LIMIT 5"
        return self.connection.cypher.execute(cypher_query)

    def get_node_by_name(self, search_input):
        cypher_query = "MATCH (n:Concept { NAME:'" + search_input + "'}) RETURN n"
        node = self.execute_query(cypher_query)
        return node.one

    def get_node_by_id(self, id):
        cypher_query = "MATCH (n) WHERE id(n)=" + id + " RETURN n"
        return self.execute_query(cypher_query)

    def get_direct_edges(self, node):
        cypher_query = "MATCH (n:Concept { CUI:'" + node.properties['CUI'] + "'})-[r]-c RETURN r"
        return self.execute_query(cypher_query)

    def get_direct_nodes(self, node):
        cypher_query = "MATCH (n:Concept { CUI:'" + node.properties['CUI'] + "'})-[r]-c RETURN c"
        return self.execute_query(cypher_query)

    def get_edges_between_nodes(self, node1, node2):
        # Not necessarily one edge between nodes can't take [0] need to specify rel label
        cypher_query = "MATCH (n:Concept { CUI:'" + node1.properties['CUI'] + "'})-[r]-(c { CUI:'" + node2.properties['CUI'] + "'})" + "RETURN r"
        return self.execute_query(cypher_query)