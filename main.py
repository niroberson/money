from analysis import Analyzer


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self):
        self.Analyzer = Analyzer()

    def add_distance_field_to_graph(self):
        pass

if __name__ == "__main__":
    RecommenderFactory()