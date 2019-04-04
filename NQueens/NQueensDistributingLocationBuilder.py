import random

from Framework.Genetics.LocationBuildController import LocationBuildController
from Framework.Genetics.LocationBuilder import LocationBuilder
from NQueens.LocationCreators.CrossOverLocationBuilder import CrossOverLocationBuilder
from NQueens.NQueensHistoryDuplicateLocationBuilder import NQueensHistoricalDuplicateLocationBuilder


class NQueensDistributingLocationBuilder(LocationBuildController):

    def __init__(self, parameters, location_builders, history_dim):
        super(NQueensDistributingLocationBuilder, self).__init__(parameters, location_builders)
        self.duplicate_builder = NQueensHistoricalDuplicateLocationBuilder(parameters, location_builders, history_dim)
        self.cross_over_builder = NQueensHistoricalDuplicateLocationBuilder(parameters, location_builders, history_dim)#CrossOverLocationBuilder(parameters) #NQueensHistoricalDuplicateLocationBuilder(parameters, location_builders, history_dim-1)
        self.genetic_builder = NQueensHistoricalDuplicateLocationBuilder(parameters, location_builders, history_dim) #LocationBuilder(parameters)
        self.requests = 0
        self.bias = parameters.bias
        self.parameters = parameters

    def build(self, build_params):
        self.requests += 1
        if self.duplicate_builder.completed_loop and (self.requests % self.parameters.request_mod == 0) and (self.bias[0] > self.parameters.bias_min):
            self.bias[0] -= 2
            self.bias[1] -= 1

        index = random.randint(0, self.bias[2])

        if index < self.bias[0]:
            return self.duplicate_builder.build(build_params)

        if index < (self.bias[0] + self.bias[1]):
            return self.cross_over_builder.build(build_params)

        return self.genetic_builder.build(build_params)