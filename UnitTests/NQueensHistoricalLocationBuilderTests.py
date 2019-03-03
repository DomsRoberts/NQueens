import unittest

from Framework.Configuration.RunParameters import RunParameters
from NQueens.NQueensHistoricalLocationBuilder import NQueensHistoricalLocationBuilder
from NQueens.NQueensHistoryDuplicateLocationBuilder import NQueensHistoricalDuplicateLocationBuilder


class NQueensHistoricalLocationBuilderTests(unittest.TestCase):

    def test_import_dimension_file(self):
        parameters = RunParameters(8, [8, 8, 8, 8, 8, 8, 8, 8])
        loc_builder = NQueensHistoricalLocationBuilder(parameters, [], isTest=True)

        cell_store = loc_builder.import_file(7)

        self.assertGreater(1, len(cell_store))

    def test_import_dimension_file_not_existent(self):
        parameters = RunParameters(8, [8, 8, 8, 8, 8, 8, 8, 8])
        loc_builder = NQueensHistoricalLocationBuilder(parameters, [], isTest=True)

        cell_store = loc_builder.import_file(99)

        self.assertEqual(99, len(cell_store))

    def test_that_Scaling_to_fit_will_merge_values_to_larger_table(self):
        parameters = RunParameters(8, [8, 8, 8, 8, 8, 8, 8, 8])
        loc_builder = NQueensHistoricalLocationBuilder(parameters, [], isTest=True)

        cell_store = loc_builder.import_file(7)

        scaled = loc_builder.scale_to_fit(8,7,cell_store)
        self.assertEqual(8, len(scaled))

    def test_that_the_chance_array_is_created_on_construction(self):
        parameters = RunParameters(8, [8, 8, 8, 8, 8, 8, 8, 8])
        loc_builder = NQueensHistoricalLocationBuilder(parameters, [], 7)

        self.assertEqual(8, len(loc_builder.cell_table))

    def test_that_building_a_location_will_create_a_valid_location(self):
        parameters = RunParameters(8, [8, 8, 8, 8, 8, 8, 8, 8])
        loc_builder = NQueensHistoricalLocationBuilder(parameters, [], 7)

        location = loc_builder.build(None)
        self.assertEqual(8, len(location))

    def test_that_the_duplicate_builder_can_build_a_location(self):
        parameters = RunParameters(8, [8, 8, 8, 8, 8, 8, 8, 8])
        loc_builder = NQueensHistoricalDuplicateLocationBuilder(parameters, [], 7)

        new_loc = loc_builder.build(None)

        self.assertEqual(8, len(new_loc))
