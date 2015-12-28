from graph import Graph
from results import Results
from pandas import DataFrame


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, dev_flag):
        self.graph = Graph(dev_flag)

    def search_concept(self, concept):
        concept_node = self.graph.get_node_by_name(concept)
        self.graph.create_subgraph(concept_node)

        paths, path_lengths = self.graph.get_shortest_paths(concept_node)
        path_nodes = path_lengths.keys()
        names = [self.graph.node[nodeX]['properties']['NAME'] for nodeX in path_nodes]
        # Return a table sorted by shortest path lengths
        data = {'Concept': names,
                'Distance': list(path_lengths.values()), 'Path': list(paths.values())}
        df = DataFrame(data, index=path_nodes)
        df = df.sort('Distance')
        results = Results(df)
        error = None
        return results, error


