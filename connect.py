from py2neo import Graph
__author__ = 'nathir2'


class Database:
    def __init__(self):
        self.user = "neo4j"
        self.password = "newk1ng$!"
        self.host_local = "localhost:7474/db/data"

    def connect_local(self):
        endpoint = Database.create_endpoint(self.host_local, self.user, self.password)
        return Graph(endpoint)

    @staticmethod
    def create_endpoint(host, user, password):
        return "http://" + user + ":" + password + "@" + host