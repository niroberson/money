from pandas import DataFrame


class Results:
    def __init__(self, names, paths):
        # Get a dictionary of the shortest paths based on this node
        distances = paths.values()
        # Return a table sorted by shortest path lengths
        self.df = DataFrame([names, distances], columns=['Concept', 'distance'])

    def as_table(self):
        # Create table from distance results
        pass

    def as_graph(self):
        # Display results as graph with cytoscape or something
        pass
