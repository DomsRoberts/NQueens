import random


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
        convertedValue = self.convertToEvaluationFormat(self.currentLocation)
        result = evaluator.evaluate(convertedValue)

        if result < self.bestPerformance:
            self.bestPerformance = result
            self.bestLocation = self.currentLocation

        return result

    def selectLocation(self, demeLocation):
        currentLocation = demeLocation
        mutationsRemaining = self.mutationCount
        while mutationsRemaining > 0:
            currentLocation = self.performMutation(currentLocation)
            mutationsRemaining -= 1

        return currentLocation

    def performMutation(self, location):
        insertPosition = random.randint(0, len(location) - 1)
        newChar = self.selectNewNode(insertPosition)

        start = location[:insertPosition] if insertPosition > 0 else ""
        end = location[insertPosition + 1:] if insertPosition < (len(location)- 1) else ""
        newLocation = start + newChar + end
        return newLocation

    def selectNewNode(self, index):
        bounds = self.parameters.bounds[index]
        value = random.randint(0, bounds - 1)
        return chr(ord('A') + value)

    def convertToEvaluationFormat(self, location):
        converted = [ord(c) - ord('A') for c in location]
        return converted