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

        crossed_deme_index = random.randint(0, member_count - 1)
        crossed_deme = self.deme_controller.members[crossed_deme_index]
        crossed_location = crossed_deme.bestLocation

        new_location = GeneticFunctions.create_crossover(demeLocation, crossed_location)
        return super(NQueensGeneticMember, self).selectLocation(new_location)
