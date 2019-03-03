from Framework.LocationStore import LocationStore


class NQueensLocationStore(LocationStore):

    def __init__(self, parameters):
        super(NQueensLocationStore, self).__init__(parameters)
        self.cell_count = {}
        for x in range(0, parameters.dimensions):
            self.cell_count[x] = [0 for y in range(0, self.parameters.dimensions)]

    def insert(self, location, value):
        if location not in self.location_store:
            self.location_store[location] = value
            self.locations.append(location)
            if value == 0:
                self.insert_correct_value_to_cells(location)

    def insert_correct_value_to_cells(self, location):
        for col in range(0, self.parameters.dimensions):
            cell_array = self.cell_count[col]
            cell_index = self.convert_to_index(location[col])
            cell_array[cell_index] += 1

    @staticmethod
    def convert_to_index(char):
        index = ord(ord(char) - ord('A'))
        return index
