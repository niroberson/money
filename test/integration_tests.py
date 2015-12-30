from factory import RecommenderFactory
from config import Config

if __name__ == "__main__":
    config = Config()
    rf = RecommenderFactory(config, True)
    rf.search_concept('BRCA1')