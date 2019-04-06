import math

from Framework.Configuration.RunParameters import RunParameters
from Framework.Genetics.LocationBuilder import LocationBuilder
from NQueens.LocationCreators.CrossOverLocationBuilder import CrossOverLocationBuilder
from NQueens.NQueensDistributingLocationBuilder import NQueensDistributingLocationBuilder
from NQueens.NQueensHistoricalLocationBuilder import NQueensHistoricalLocationBuilder
from NQueens.NQueensHistoryDuplicateLocationBuilder import NQueensHistoricalDuplicateLocationBuilder


class NQueensRunParameters(RunParameters):

    def __init__(self, dimensions, bounds, prune_age, mutation_count, distribution_bias, tournament_size, prune_size, import_dimensions, use_random):
        super(NQueensRunParameters, self).__init__(dimensions, bounds)

        self.total_demes = dimensions * 10
        self.use_random = use_random
        self.deme_size = dimensions
        self.mutation_count = mutation_count
        self.prune_size = prune_size
        self.bias = distribution_bias
        self.tournament_size = tournament_size
        self.prune_age = prune_age #math.pow(dimensions, 2)
        #self.location_builders = [CrossOverLocationBuilder(self)] #[NQueensDistributingLocationBuilder(self, [], dimensions - 1)]
        #self.location_builders = [CrossOverLocationBuilder(self)]
        self.location_builders = [NQueensDistributingLocationBuilder(self, [], import_dimensions)]
    #[CrossOverLocationBuilder(self),
