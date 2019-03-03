from Framework.Genetics import GeneticFunctions


class LocationBuilder:

    def __init__(self, parameters):
        self.parameters = parameters

    def build(self, build_params):
        return GeneticFunctions.create_random_location(self.parameters.dimensions)
