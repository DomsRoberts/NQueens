from Framework.Genetics.LocationBuildController import LocationBuildController
from Framework.RunController import RunController
from NQueens.LocationCreators.NQueensLocationBuilderParameters import NQueensLocationBuilderParameters
from NQueens.NQueensDemeBuilder import NQueensDemeBuilder
from NQueens.NQueensHistoricalLocationBuilder import NQueensHistoricalLocationBuilder

from NQueens.NQueensLocationBuildController import NQueensLocationBuildController
from NQueens.NQueensLocationStore import NQueensLocationStore


class NQueensRunController(RunController):

    def __init__(self, parameters):
        super(NQueensRunController, self).__init__(parameters, NQueensLocationStore(parameters))
        self.parameters = parameters
        self.foundResults = []
        self.demes = []
        self.locationBuildController = LocationBuildController(parameters, parameters.location_builders) #NQueensLocationBuildController(parameters, parameters.location_builders)
        self.demeBuilder = NQueensDemeBuilder(parameters, self.locationBuildController, self)
        self.demes = self.initialiseDemes(parameters)
        self.deme_locations = {}

    def update(self, problem):
        super(NQueensRunController, self).update(problem)
        for deme in self.demes:
            deme.evaluate(problem)
            deme.update()
            if len(deme.members) == 0:
                self.demes.remove(deme)
                self.insertNewDeme()

    def insertNewDeme(self):
        build_params = NQueensLocationBuilderParameters(self.location_store)
        newDeme = self.demeBuilder.build_with_location(build_params)
        self.demes.append(newDeme)

    def initialiseDemes(self, parameters):
        return [self.demeBuilder.build() for x in range(0, parameters.total_demes)]