import networkx as nx


class Concept:
    def __init__(self, properties):
        self.id = properties['ID']
        self.name = properties['NAME']
        self.cui = properties['CUI']


class Relationship:
    def __init__(self, properties):
        self.predication_name = properties['NAME']
        self.predication_id = properties['ID']
        self.source_node = Concept(properties.source_node)
        self.target_node = Concept(properties.target_node)


class Graph:
    # Build a networkX graph from concepts and relationships
    def __init__(self):
        self.graph = nx.Graph()

    def create_graph(self, nodes, distances):
        # Format : [(a,b, dist), (b,c, dist)]
        self.graph.add_nodes_from([nodes])
        self.graph.add_weighted_edges_from(distances)

    def analyze(self, source_node):
        paths = nx.single_source_dijkstra_path(self.graph, source_node)
        lengths = nx.single_source_dijkstra_path_length(self.graph, source_node)

