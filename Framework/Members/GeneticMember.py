import random

from Framework.Genetics import GeneticFunctions


class GeneticMember:

    def __init__(self, parameters, demeLocation, mutationCount):
        self.parameters = parameters
        self.bestPerformance = 9999999999
        self.mutationCount = mutationCount
        self.initialLocation = self.selectLocation(demeLocation)
        self.currentLocation = self.initialLocation
        self.bestLocation = self.currentLocation
        self.age = 0

    def get_BestFitness(self):
        return self.bestPerformance

    def update(self):
        self.currentLocation = self.selectLocation(self.currentLocation)
        self.age += 1

    def evaluate(self, evaluator):
        result = evaluator.evaluate(self.currentLocation)

        if result < self.bestPerformance:
            self.bestPerformance = result
            self.bestLocation = self.currentLocation

        return result

    def selectLocation(self, demeLocation):
        currentLocation = demeLocation
        currentLocation = GeneticFunctions.switch_positions(currentLocation, self.mutationCount)

        return currentLocation