from factory import RecommenderFactory


if __name__ == "__main__":
    rf = RecommenderFactory(True)
    results, error = rf.search_concept('BRCA1')
    print(results.df)
