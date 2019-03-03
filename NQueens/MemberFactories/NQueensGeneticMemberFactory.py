from Framework.Genetics import GeneticFunctions
from Framework.MemberFactories.GeneticMemberFactory import GeneticMemberFactory
from NQueens.NQueensGeneticMenber import NQueensGeneticMember


class NQueensGeneticMemberFactory(GeneticMemberFactory):

    def __init__(self, parameters):
        super(NQueensGeneticMemberFactory, self).__init__(parameters)

    def build(self, deme_location, location_store):
        random_location = GeneticFunctions.create_random_location(self.parameters.dimensions) #location_store.select_at_random()
        new_location = GeneticFunctions.create_crossover(deme_location, random_location)
        return NQueensGeneticMember(self.parameters, new_location, self.parameters.mutation_count)
