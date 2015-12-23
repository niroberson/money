
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

