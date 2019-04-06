from Framework.Genetics import GeneticFunctions
from Framework.MemberFactories.GeneticMemberFactory import GeneticMemberFactory
from NQueens.NQueensGeneticMenber import NQueensGeneticMember


class NQueensGeneticMemberFactory(GeneticMemberFactory):

    def __init__(self, parameters):
        super(NQueensGeneticMemberFactory, self).__init__(parameters)

    def build(self, deme_location, location_store):
        new_location = GeneticFunctions.switch_positions(deme_location, 3)
        return NQueensGeneticMember(self.parameters, new_location, self.parameters.mutation_count)
