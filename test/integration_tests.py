from factory import RecommenderFactory
from config import Config


def test_traversal():
    config = Config(False)
    rf = RecommenderFactory(config)
    rf.traverse_edges_to_neo()


def test_node_traversal():
    config = Config(False)
    rf = RecommenderFactory(config)
    rf.traverse_nodes()


def test_viz():
    config = Config()
    rf = RecommenderFactory(config)
    concept = 'BRCA1'
    results, error = rf.search_concept(concept)
    results.to_graph_json()


def test_results():
    config = Config()
    rf = RecommenderFactory(config)
    concept = 'BRCA1'
    results, error = rf.search_concept(concept)
    print(results.table)


def test_search_concept_object():
    config = Config()
    rf = RecommenderFactory(config)
    concept = 'BRCA1'
    object = 'Mitochondria'
    results = rf.search_concept_object(concept, object)
    print(results.table)

if __name__ == "__main__":
    test_traversal()