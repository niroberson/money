from database import Database


class Analyzer:
    def __init__(self):
        self.datbase = Database()

    @staticmethod
    def compute_distance(database, node_source, node_target):
        print('Calculating distance between %s and %s' % (node_source.properties['NAME'], node_target[0].properties['NAME']))
        n_i = database.get_count_direct_edges(node_source)
        n_j = database.get_count_direct_edges(node_target)
        n_i_j = database.get_count_between_nodes(node_source, node_target)
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = ([1/ksp - 1])
        return d
