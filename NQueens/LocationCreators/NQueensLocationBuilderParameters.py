from Framework.Genetics.LocationBuilderParameters import LocationBuilderParameters


class NQueensLocationBuilderParameters(LocationBuilderParameters):

    def __init__(self, location_store):
        super(NQueensLocationBuilderParameters, self).__init__()
        self.location_store = location_store