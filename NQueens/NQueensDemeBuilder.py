from Framework.MemberFactories.GeneticMemberFactory import GeneticMemberFactory
from NQueens.LocationCreators.NQueensLocationBuilderParameters import NQueensLocationBuilderParameters
from NQueens.MemberFactories.NQueensGeneticMemberFactory import NQueensGeneticMemberFactory
from NQueens.MemberFactories.NQueensRandomLocationMemberFactory import NQueensRandomLocationMemberFactory
from NQueens.MemberFactories.NQueensRandomMutationMemberFactory import NQueensRandomMutationMemberFactory
from NQueens.MemberFactories.NQueensReverseMutationMemberFactory import NQueensReverseMutationMemberFactory
from NQueens.NQueensDemeController import NQueensDemeController


class NQueensDemeBuilder:

    def __init__(self, parameters, locationBuildController, run_controller):
        self.parameters = parameters
        self.demes = []
        self.run_controller = run_controller
        self.locationBuildController = locationBuildController
        self.success_monitor = {}

    def build(self):
        build_param = NQueensLocationBuilderParameters(self.run_controller.location_store)
        return NQueensDemeController(self.parameters, self.get_memberFactories(), self.locationBuildController, self.run_controller.location_store, build_param)

    def build_with_location(self, build_param):
        return NQueensDemeController(self.parameters, self.get_memberFactories(), self.locationBuildController, self.run_controller.location_store, build_param)

    def get_memberFactories(self):
        return [GeneticMemberFactory(self.parameters),
                NQueensRandomMutationMemberFactory(self.parameters),
                NQueensGeneticMemberFactory(self.parameters)]
               # NQueensRandomLocationMemberFactory(self.parameters),
            #    NQueensRandomMutationMemberFactory(self.parameters)]
        #return [#NQueensRandomMutationMemberFactory(self.parameters),
         #       NQueensReverseMutationMemberFactory(self.parameters),
          #      NQueensRandomLocationMemberFactory(self.parameters)]