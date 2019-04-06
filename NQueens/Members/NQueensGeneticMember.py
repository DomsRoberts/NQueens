import random

from Framework.Genetics import GeneticFunctions
from Framework.Members.GeneticMember import GeneticMember


class NQueensGeneticMember(GeneticMember):

    def __init__(self, parameters, demeLocation, mutationCount):
        super(NQueensGeneticMember, self).__init__(parameters, demeLocation, mutationCount)

    def selectLocation(self, demeLocation):
        member_count = len(self.deme_controller.members)
        if member_count == 1:
            return super(NQueensGeneticMember, self).selectLocation(demeLocation)

        new_location = GeneticFunctions.switch_positions(demeLocation, self.mutationCount)
        return super(NQueensGeneticMember, self).selectLocation(new_location)
