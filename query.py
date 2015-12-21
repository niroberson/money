from connect import Database
__author__ = 'nathir2'


class Query:
    def __init__(self):
        self.db = Database().connect_local()