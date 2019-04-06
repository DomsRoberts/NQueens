import random

from Framework.Genetics import GeneticFunctions
from Framework.Genetics.LocationBuilder import LocationBuilder


class CrossOverLocationBuilder(LocationBuilder):

    def __init__(self, parameters):
        super(CrossOverLocationBuilder, self).__init__(parameters)

    def build(self, build_params):
        location_store = build_params.location_store
        total_available = len(location_store.locations)

        deme_one_best = self.select_new_location(location_store, total_available)

        cross_location = GeneticFunctions.switch_positions(deme_one_best, self.parameters.dimensions / 2)
        return cross_location

    def select_new_location(self, location_store, total_available):
        test1 = random.randint(1, 2)
        deme_one_best = self.select_random_best(total_available, location_store) \
            if total_available > 1 and test1 == 1 \
            else self.select_random_location()
        return deme_one_best

    @staticmethod
    def select_random_best(total_available, location_store):
        choice_one = random.randint(0, total_available - 1)
        deme_one = location_store.locations[choice_one]
        deme_one_best = deme_one.bestLocation
        return deme_one_best

    def select_random_location(self):
        return GeneticFunctions.create_random_location(self.parameters.dimensions)

