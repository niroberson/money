from factory import RecommenderFactory
import os
from config import Config

if __name__ == "__main__":
    config = Config()
    rf = RecommenderFactory(True, config)
    results, error = rf.search_concept('BRCA1')
    results.to_graph()
    results.to_graph_json()
