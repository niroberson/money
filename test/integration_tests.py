from factory import RecommenderFactory


if __name__ == "__main__":
    rf = RecommenderFactory(True)
    rf.search_concept('BRCA1')
