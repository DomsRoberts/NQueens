import random

from Framework.Genetics import GeneticFunctions
from NQueens.NQueensHistoricalLocationBuilder import NQueensHistoricalLocationBuilder


class NQueensHistoricalDuplicateLocationBuilder(NQueensHistoricalLocationBuilder):

    def __init__(self, parameters, location_builder, history_dim, isTest = False):
        super(NQueensHistoricalDuplicateLocationBuilder, self).__init__(parameters, location_builder, history_dim, isTest)
        self.requests = 0
        self.seed_length = history_dim
        self.import_row_count = len(self.import_rows)
        self.completed_loop = False

    def build(self, build_params):
        self.requests += 1
        if self.requests >= self.import_row_count:
            self.completed_loop = True
            self.requests = 0
        location = ""
        seed_indexes = self.select_seed()
        seed_location = [self.convert_to_char(x) for x in seed_indexes]
        random_location = GeneticFunctions.create_random_location(self.parameters.dimensions)
        diff = self.parameters.dimensions - self.seed_length
        x_offset = random.randint(0, diff - 1)
        y_offset = random.randint(0, diff - 1)
        for x in range(0, self.parameters.dimensions):
            source = random_location if (x < x_offset or
                                         x >= (x_offset + self.seed_length)) else seed_location
            value = source[x - x_offset] if (x >= x_offset or x <= (x_offset + self.seed_length)) else source[x]
            location = location + value

        return location

    def select_seed(self):
        index = self.requests
        return self.import_rows[index]