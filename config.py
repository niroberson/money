import os


class Config:
    def __init__(self, dev_flag=True):
        self.dev_flag = dev_flag
        self.data_dir = os.path.join(os.path.curdir, '..', 'static')
        self.host_local = "localhost:7474/db/data"
        self.host_remote = "96.241.238.159:7474/db/data"
        self.user = "neo4j"
        self.pw = "test"

