import random


class LocationBuildController:

    def __init__(self, parameters, locationBuilders):
        self.parameters = parameters
        self.location_builders = locationBuilders

    def build(self, build_params):
        builderIndex = random.randint(0, len(self.location_builders) - 1)
        builder = self.location_builders[builderIndex]

        return builder.build(build_params)
