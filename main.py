from analysis import Analyzer


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self):
        self.Analyzer = Analyzer()

    def add_distance_field_to_graph(self):
        pass

    def search_keyword(self, keyword):
        results = self.Analyzer.compute_distances_single_source_node(keyword)



if __name__ == "__main__":
    rf = RecommenderFactory()
    rf.search_keyword('BRCA1')
