import random

from Framework.Genetics import GeneticFunctions


class LocationStore:

    def __init__(self, parameters):
        self.parameters = parameters
        self.location_store = {}
        self.locations = []
        
    def insert(self, location, value):
        if location not in self.location_store:
            self.location_store[location] = value
            self.locations.append(location)

    def select_at_random(self):
        if len(self.location_store) == 0:
            return GeneticFunctions.create_random_location(self.parameters.dimensions)

        index = random.randint(0, len(self.location_store) - 1)

        return self.locations[index]

