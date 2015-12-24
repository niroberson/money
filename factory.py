from analysis import Analyzer

class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self):
        self.Analyzer = Analyzer()

    def add_distance_field_to_graph(self):
        pass

    def search_keyword(self, keyword):
        # If node is not found by keyword, return an error
        results = None
        error = None
        try:
            node_of_interest = self.Analyzer.search_nodes(keyword)
        except IndexError:
            error = 'A node does not exist for this keyword'
        else:
            results = self.Analyzer.compute_distances_single_source_node(node_of_interest)
        return results, error