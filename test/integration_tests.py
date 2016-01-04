from factory import RecommenderFactory
from config import Config


def test_traversal():
    config = Config()
    rf = RecommenderFactory(config)
    rf.create_distance_graph()


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

if __name__ == "__main__":
    test_results()