import random

from NQueens.NQueensEvaluation import NQueensEvaluation
from NQueens.NQueensRunController import NQueensRunController
from NQueens.NQueensRunParameters import NQueensRunParameters


class RunExecutor:

    def __init__(self):
        self.evaluation = NQueensEvaluation()
        self.dimensions = 8
        self.bounds = [self.dimensions for x in range(0, self.dimensions)]
        self.parameters = NQueensRunParameters(self.dimensions, self.bounds, 1, 1, [], 2, 1)
        self.prune_ages = [10, 15,  20, 25,  30, 35,  40, 45,  50, 55, 60, 65, 70]

    def execute_single(self):
        dimensions = 8
        self.bounds = [dimensions for x in range(0, dimensions)]
        bias = [90, 95, 100]
        self.parameters = NQueensRunParameters(dimensions, self.bounds, 65, 2, bias, 3, 2)
        self.parameters.request_mod = dimensions * 7.5
        self.parameters.bias_min = 40
        controller = NQueensRunController(self.parameters)
        print("=============" + str(65) + "=====" + str(2) + " :: " + str(bias[0]) + " :: " + str(
            bias[1]) + " :: " + str(bias[2]))

        timeSinceUpdate = 0
        previousSize = 0
        for iteration in range(0, self.parameters.maxIterations):
            controller.update(self.evaluation)
            currentSize = len(self.evaluation.resultStore)
            if currentSize == previousSize:
                timeSinceUpdate += 1

            previousSize = currentSize
            if len(controller.demes) == 0:
                break
            if timeSinceUpdate > 2000: # + (2000 * loop):
                break
            # if len(self.evaluation.resultStore) == 92:
        #      break

        #        for value in self.evaluation.resultStore:
        #            print(value)

        print(str(dimensions) + "======== " + str(len(self.evaluation.resultStore)) + "=======")

        self.output_to_file()

    def execute(self):
       # try:
        for loop in range(10, 100):
            self.evaluation = NQueensEvaluation()
            prune_age = 20 + (loop * 5)#self.prune_ages[loop % len(self.prune_ages)]
            mutation_count = loop / 2#random.randint(0, 8)
            min_age = 56 + loop # 50 + random.randint(0, 40)
            diff = 10#random.randint(0, 15)
            bias = [min_age, min_age + diff, min_age + diff + diff]
            self.bounds = [loop for x in range(0, loop)]
            self.parameters = NQueensRunParameters(loop, self.bounds, prune_age, mutation_count, bias, 5, 3)
            self.parameters.request_mod = loop * 7.5
            self.parameters.bias_min = 40
            controller = NQueensRunController(self.parameters)
            print("=============" + str(prune_age) + "=====" + str(mutation_count) + " :: " + str(bias[0]) + " :: " + str(bias[1]) + " :: " + str(bias[2]))

            timeSinceUpdate = 0
            previousSize = 0
            for iteration in range(0, self.parameters.maxIterations):
                controller.update(self.evaluation)
                currentSize = len(self.evaluation.resultStore)
                if currentSize == previousSize:
                    timeSinceUpdate += 1

                previousSize = currentSize
                if len(controller.demes) == 0:
                    break
                if timeSinceUpdate > 500 + (2000 * loop):
                    break
                #if len(self.evaluation.resultStore) == 92:
              #      break

    #        for value in self.evaluation.resultStore:
    #            print(value)

            print(str(loop) + "======== " + str(len(self.evaluation.resultStore)) + "=======")

            self.output_to_file()

    def output_to_file(self):
        filename = str(self.parameters.dimensions) + "output.txt"
        f = open(filename, "w")
        for value in self.evaluation.resultStore:
            f.write(value)
            f.write("\r")
        f.close()

    #    except Exception:
     #       pass

