import random
from Framework.MemberFactories.GeneticMemberFactory import GeneticMemberFactory
from NQueens.NQueensGeneticMenber import NQueensGeneticMember


class NQueensRandomMutationMemberFactory(GeneticMemberFactory):

    def __init__(self, parameters):
        super(NQueensRandomMutationMemberFactory, self).__init__(parameters)

    def build(self, deme_location, location_store):
        mutations = random.randint(1, self.parameters.dimensions - 1)
        return NQueensGeneticMember(self.parameters, deme_location, mutations)
