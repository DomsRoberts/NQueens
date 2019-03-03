import random
from Framework.MemberFactories.GeneticMemberFactory import GeneticMemberFactory
from NQueens.NQueensGeneticMenber import NQueensGeneticMember


class NQueensReverseMutationMemberFactory(GeneticMemberFactory):

    def __init__(self, parameters):
        super(NQueensReverseMutationMemberFactory, self).__init__(parameters)

    def build(self, deme_location, location_store):
        location = deme_location[::-1]
        return NQueensGeneticMember(self.parameters, location, self.parameters.mutation_count)
