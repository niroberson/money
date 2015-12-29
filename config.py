import os


class Config:
    def __init__(self):
        self.data_dir = os.path.join(os.path.curdir, '..', 'static')
        self.host_local = "localhost:7474/db/data"
        self.user = "neo4j"
        self.pw = "test"

