import math

from Framework.Configuration.RunParameters import RunParameters
from Framework.Genetics.LocationBuilder import LocationBuilder
from NQueens.LocationCreators.CrossOverLocationBuilder import CrossOverLocationBuilder
from NQueens.NQueensDistributingLocationBuilder import NQueensDistributingLocationBuilder
from NQueens.NQueensHistoricalLocationBuilder import NQueensHistoricalLocationBuilder
from NQueens.NQueensHistoryDuplicateLocationBuilder import NQueensHistoricalDuplicateLocationBuilder


class NQueensRunParameters(RunParameters):

    def __init__(self, dimensions, bounds, prune_age, mutation_count, distribution_bias, tournament_size, prune_size):
        super(NQueensRunParameters, self).__init__(dimensions, bounds)

        self.total_demes = dimensions * 10
        self.deme_size = dimensions
        self.mutation_count = mutation_count
        self.prune_size = prune_size
        self.bias = distribution_bias
        self.tournament_size = tournament_size
        self.prune_age = prune_age #math.pow(dimensions, 2)
        self.location_builders = [NQueensDistributingLocationBuilder(self, [], dimensions - 1)]
            #[CrossOverLocationBuilder(self),
             #                     LocationBuilder(self)]
            #[historical]
            #, historical, historical,
             #                     CrossOverLocationBuilder(self),
            #                      LocationBuilder(self)]
