from pandas import DataFrame


class Results:
    def __init__(self, graph, paths):
        path_nodes = paths.keys()
        names = [graph.node[nodeX]['properties']['NAME'] for nodeX in path_nodes]
        # Get a dictionary of the shortest paths based on this node
        distances = list(paths.values())
        # Return a table sorted by shortest path lengths
        data = {'Concept': names, 'Distances': distances}
        self.df = DataFrame(data)

    def to_html(self):
        # Create table from distance results
        return self.df.to_html()

    def to_graph(self):
        # Display results as graph with cytoscape or something
        pass
