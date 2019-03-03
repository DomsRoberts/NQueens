

class DemeController:

    def __init__(self, parameters, locationBuildController, location_store, build_params):
        self.parameters = parameters
        self.bestFitness = 9999999999
        self.bestLocation = locationBuildController.build(build_params)
        self.location_store = location_store
        self.locationBuildController = locationBuildController
        self.members = []
        self.member_pairs = []

    def initialise(self):
        self.members = self.initialise_members()

    def initialise_members(self):
        memberBuilder = self.get_memberBuilder()
        memberList = []
        diff = self.parameters.deme_size % self.parameters.tournament_size
        build_size = self.parameters.deme_size + diff

        for item in range(0, build_size, self.parameters.tournament_size):
            demeLocation = self.bestLocation if len(self.bestLocation) > 0 else self.selectNewLocation()
            tournament = [memberBuilder.build(demeLocation, self.location_store) for x in range(0, self.parameters.tournament_size)]
            self.member_pairs.append(tournament)
            for item in tournament:
                memberList.append(item)

        return memberList

    def update(self):
        for pair in self.member_pairs:
            ordered = sorted(pair, key=lambda x: x.bestPerformance)
            best_member = ordered[0]
            length = len(ordered)
            start = length - self.parameters.prune_size

            for index in range(start, length):
                remove_item = ordered[index]
                pair.remove(remove_item)
                self.members.remove(remove_item)
                member_builder = self.get_memberBuilder()
                new_member = member_builder.build(best_member.bestLocation, self.location_store)
                self.members.append(new_member)
                pair.append(new_member)

            best_member.update()

    def execute_evaluations(self, items, evaluator):
        for member in items:
            member.evaluate(evaluator)

    def evaluate(self, evaluator):
        self.execute_evaluations(self.members, evaluator)

        bestMember = self.calculateBestMember()
        if bestMember is not None:
            self.bestFitness = bestMember.get_BestFitness()
            self.bestLocation = bestMember.bestLocation

    def calculateBestMember(self):
        if len(self.members) == 0:
            return None
        sortedMembers = sorted(self.members, key=lambda k: k.get_BestFitness())
        return sortedMembers[0]

    def selectNewLocation(self):
        return self.locationBuildController.build()

    def get_memberBuilder(self):
        return None