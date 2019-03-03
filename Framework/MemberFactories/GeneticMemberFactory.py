from Framework.MemberFactories.MemberFactory import MemberFactory
from Framework.Members.GeneticMember import GeneticMember


class GeneticMemberFactory(MemberFactory):

    def __init__(self, parameters):
        self.parameters = parameters

    def build(self, demeLocation, location_store):
        return GeneticMember(self.parameters, demeLocation, 1)