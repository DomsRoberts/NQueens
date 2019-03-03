from Framework.Genetics.LocationBuildController import LocationBuildController


class NQueensLocationBuildController(LocationBuildController):

    def __init__(self, parameters, locationBuilders):
        super(NQueensLocationBuildController, self).__init__(parameters, locationBuilders)
        self.built_locations = {}
        self.rejected = 0

    def build(self, build_params):
        unique_build = False
        loop = 0
        while not unique_build:
            self.rejected += loop
            location = super(NQueensLocationBuildController, self).build(build_params)
            unique_build = location not in self.built_locations
            loop = 1

        self.built_locations[location] = True

        return location
