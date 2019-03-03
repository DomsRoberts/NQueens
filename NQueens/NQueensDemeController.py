import math
import random
from Framework.DemeControllers.DemeController import DemeController


class NQueensDemeController(DemeController):

    def __init__(self, parameters, memberFactories, locationBuildController, location_store, build_params):
        super(NQueensDemeController, self).__init__(parameters, locationBuildController, location_store, build_params)
        self.member_factories = memberFactories
        self.prune_age = parameters.prune_age
        self.successCount = 0
        self.initialise()

    def execute_evaluations(self, items, evaluator):
        for member in items:
            result = member.evaluate(evaluator)
            if result == 0:
                self.successCount += 1

    def update(self):
        super(NQueensDemeController, self).update()
        self.pruneUnsuccessfulMembers()

    def pruneUnsuccessfulMembers(self):
        count = len(self.member_pairs)
        toPrune = []
        for index in range(0, count):
            pair = self.member_pairs[index]
            if self.is_set_too_old(pair):
                toPrune.append(index)

        if len(toPrune) > 0:
            for index in range(len(toPrune)-1, 0, -1):
                remove_pair = self.member_pairs[toPrune[index]]
                self.member_pairs.remove(remove_pair)
                for item in range(0, len(remove_pair)):
                    self.members.remove(remove_pair[item])

            if len(toPrune) == 1:
                self.members.clear()
                self.member_pairs.clear()

    def get_memberBuilder(self):
        index = random.randint(0, len(self.member_factories) - 1)
        return self.member_factories[index]

    def is_set_too_old(self, pair):
        eldest = max(pair, key=lambda x: x.age)
        return eldest.age > self.parameters.prune_age