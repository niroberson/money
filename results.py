from pandas import DataFrame


class Results:
    def __init__(self, df):
        self.df = df

    def to_html(self):
        # Create table from distance results
        return self.df.to_html()

    def to_graph(self):
        # Display results as graph with cytoscape or something
        pass
