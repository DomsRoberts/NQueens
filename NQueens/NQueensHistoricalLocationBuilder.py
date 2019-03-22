import math
import random

from Framework.Genetics.LocationBuildController import LocationBuildController


class NQueensHistoricalLocationBuilder(LocationBuildController):

    def __init__(self, parameters, location_builder, history_dim, isTest = False):
        super(NQueensHistoricalLocationBuilder, self).__init__(parameters, location_builder)
        lower_dimensions = history_dim
        if isTest is False:
            self.import_rows = self.import_file(lower_dimensions)
            self.import_table = self.import_cell_store(lower_dimensions, self.import_rows)
            if len(self.import_table) > 0:
                self.cell_store = self.scale_to_fit(parameters.dimensions, lower_dimensions, self.import_table)
            else:
                self.cell_store = self.create_empty_cell_store(parameters.dimensions, parameters.dimensions)

            self.cell_table = self.build_chance_table(parameters.dimensions, self.cell_store)

    def build(self, build_params):
        location = ""
        for x in range(0, self.parameters.dimensions):
            index = self.select_location(self.parameters.dimensions, x)
            char = self.convert_to_char(index)
            location = location + char

        return location

    def scale_to_fit(self, dimensions, lower_dimensions, cell_table):
        scale = lower_dimensions / dimensions
        one_over = 1 - scale
        scale_values = self.create_empty_cell_store(dimensions, 0)

        for x in range(0, lower_dimensions):
            for y in range(0, lower_dimensions):
                cell_value = cell_table[x][y]
                value_to_use_left = (scale * cell_value) if y > 0 else cell_value
                value_to_use_right = (one_over * cell_value) if y < (lower_dimensions - 1) else cell_value
                scale_values[x][y] += int(math.ceil(value_to_use_left))
                scale_values[x+1][y] += int(math.ceil(value_to_use_left))
                scale_values[x][y+1] += int(math.ceil(value_to_use_right))
                scale_values[x + 1][y + 1] += int(math.ceil(value_to_use_right))

        return scale_values

    def import_file(self, import_dimensions):
        with open(str(import_dimensions) + "output.txt") as f:
            content = f.readlines()
        cell_values = []
        for row in content:
            cells = [int(c) for c in row.split('#')]
            cell_values.append(cells)

        return cell_values

    def import_cell_store(self, dimensions, cell_values):
        cell_store = self.create_empty_cell_store(dimensions, 0)

        for row in cell_values:
            for col in range(0, dimensions):
                cell_store[col][row[col]] += 1

        return cell_store

    def create_empty_cell_store(self, dimensions, fill_value):
        cell_store = {}
        for cell in range(0, dimensions):
            cell_store[cell] = [fill_value for y in range(0, dimensions)]

        return cell_store

    def build_chance_table(self, dimensions, cell_store):
        cell_table = {}
        for cell in range(0, dimensions):
            cell_table[cell] = self.create_chance_array(dimensions, cell_store[cell])

        return cell_table

    @staticmethod
    def create_chance_array(dimensions, cell_array):
        chance_array = []
        for index in range(0, dimensions):
            for t in range(0, cell_array[index]):
                chance_array.append(index)

        return chance_array

    def select_location(self, dimensions, index):
        table = self.cell_table[index]
        length = len(table)
        if length == 0:
            return random.randint(0, dimensions -1)
        rand = random.randint(0, length - 1)
        return table[rand]

    def convert_to_char(self, index):
        return chr(ord('A') + index)

    def is_not_edge_cell(self, x, y, lower_dimensions):
        edge = lower_dimensions - 1
        if 0 < y < edge:
            return True

        return False