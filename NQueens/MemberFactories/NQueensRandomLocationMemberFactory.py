from Framework.Genetics import GeneticFunctions
from Framework.MemberFactories.GeneticMemberFactory import GeneticMemberFactory
from NQueens.NQueensGeneticMenber import NQueensGeneticMember


class NQueensRandomLocationMemberFactory(GeneticMemberFactory):

    def __init__(self, parameters):
        super(NQueensRandomLocationMemberFactory, self).__init__(parameters)

    def build(self, deme_location, location_store):
        new_location = GeneticFunctions.create_random_location(self.parameters.dimensions)
        return NQueensGeneticMember(self.parameters, new_location, 1)
