from connect import Database
__author__ = 'nathir2'


class Query:
    def __init__(self):
        self.db = Database().connect_local()

    def get_node(self, search_input):
        cypher_query = "MATCH (n { NAME:'" + search_input + "'}) RETURN n"
        return self.db.cypher.execute(cypher_query)

    def get_node_rels(self, node):
        cypher_query = "MATCH (n { CUI:'" + node.properties['CUI'] + "'})-[r]-c RETURN r"
        return self.db.cypher.execute(cypher_query)

    def get_direct_nodes(self, node):
        cypher_query = "MATCH (n { CUI:'" + node.properties['CUI'] + "'})-[r]-c RETURN c"
        return self.db.cypher.execute(cypher_query)