from factory import RecommenderFactory
from config import Config


def test_traversal():
    config = Config()
    rf = RecommenderFactory(config, True)
    rf.create_distance_graph()


def test_viz():
    config = Config()
    rf = RecommenderFactory(config, False)
    concept = 'BRCA1'
    results, error = rf.search_concept(concept)
    results.to_graph()

if __name__ == "__main__":
    test_viz()