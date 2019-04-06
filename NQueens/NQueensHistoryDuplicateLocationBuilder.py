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
        location = []
        seed_indexes = self.select_seed()
        seed_location = [x for x in seed_indexes]

        diff = self.parameters.dimensions - self.seed_length
        x_offset = random.randint(0, diff - 1)

        random_location = self.create_unique_location(self.parameters.dimensions, self.seed_length, x_offset) \
            if self.parameters.use_random \
            else self.tile_location(self.parameters.dimensions, seed_location)

        for x in range(0, self.parameters.dimensions):
            source = random_location if (x < x_offset or
                                         x >= (x_offset + self.seed_length)) else seed_location
            value = source[x - x_offset] if (x >= x_offset or x <= (x_offset + self.seed_length)) else source[x]
            location.append(value)

        return location

    @staticmethod
    def create_unique_location(size, import_size, x_offset):
        random_location = GeneticFunctions.create_random_location(import_size)

        current_value = import_size
        start_val = [(current_value + x) for x in range(0,x_offset)]
        current_value = current_value + x_offset
        start_string = []
        for v in start_val:
            start_string.append(v)

        end_position = import_size + x_offset
        end_length = size - end_position
        end_val = [(current_value + x) for x in range(0, end_length)]

        end_string = []
        for v in end_val:
            end_string.append(v)

        start_string.extend(random_location)
        start_string.extend(end_string)
        return start_string

    def tile_location(self, size, location):
        destination = location
        index = random.randint(0, len(self.import_rows) - 1)
        second_indexes = self.import_rows[index]
        second_location = [x for x in second_indexes]
        length = len(location)
        remainder = size - length
        offset = length
        index = 0
        max_val = size - 1
        while index < remainder:
            value_as_int = min(max_val, (second_location[index] + offset))
            index += 1
            destination.append(value_as_int)

        return destination

    def select_seed(self):
        index = self.requests
        return self.import_rows[index]