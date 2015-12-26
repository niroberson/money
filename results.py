from pandas import DataFrame


class Results:
    def __init__(self, nodes, edges, paths):
        self.nodes = nodes
        self.edges = edges
        self.path = paths

    def as_table(self):
        # Create table from distance results
        pass

    def as_graph(self):
        # Display results as graph with cytoscape or something
        pass
