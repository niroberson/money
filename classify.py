from pandas import DataFrame


class Classify(object):

    def __init__(self, database):
        self.database = database
        features = DataFrame.from_csv('features.csv')


