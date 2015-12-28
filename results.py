from pandas import DataFrame


class Results:
    def __init__(self, path_nodes, names, path_lengths, path_names):
        data = {'Concept': names,
                'Distance': path_lengths, 'Path': path_names}
        df = DataFrame(data, index=path_nodes)
        self.df = df.sort('Distance')

    def to_html(self):
        # Create table from distance results
        return self.df.to_html()

    def to_graph(self):
        # Display results as graph with cytoscape or something
        pass
