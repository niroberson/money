from analysis import Analyzer
from pandas import DataFrame
from query import Query


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, dev_flag):
        self.query = Query(dev_flag)
        self.Analyzer = Analyzer(dev_flag)

    def compute_distances_single_source_node(self, node_of_interest):
        n_i = self.Analyzer.get_num_rels(node_of_interest)
        direct_nodes = self.Analyzer.query.get_direct_nodes(node_of_interest)
        df = DataFrame()
        for node in direct_nodes:
            dx = self.compute_distance(node_of_interest, node, n_i)
            dfx = DataFrame([[node_of_interest.properties['NAME'], node_of_interest.properties['CUI'],
                              node[0].properties['NAME'], node[0].properties['CUI'], dx]],
                            columns=['source_name', 'source_id', 'target_name', 'target_id', 'distance'])
            df = df.append(dfx)
        return df

    def search_keyword(self, keyword):
        # If node is not found by keyword, return an error
        results = None
        error = None
        try:
            node_of_interest = self.Analyzer.search_nodes(keyword)
        except IndexError:
            error = 'Error: A node does not exist for this keyword'
        else:
            results = self.Analyzer.compute_distances_single_source_node(node_of_interest)

        # Sort results by distance

        return results, error
