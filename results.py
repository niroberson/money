from pandas import DataFrame


class Results:
    def __init__(self, search_node, target_nodes, distances):
        self.search_node = search_node
        self.target_nodes = target_nodes
        self.distances = distances

    def as_table(self):
        # Create table from distance results
        pass

    def as_graph(self):
        # Display results as graph with cytoscape or something
        pass
