#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

import operator
import math
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# TODO: Is there an optimum number of values required to learn the integer
#  sequence? Test min/max???
#  Note: Have to watch that numbers don't get too large
#  and overflow the variable type size.

# Defined Integer Sequences (Test cases)
# Note these sequences are usually infinite so a limited number only have been
# incorporated for test purposes. The number of the values for each sequence
# can vary as the script will automatically adapt to the length.
# Ref: Wikipedia List of OEIS Sequences
# (https://en.wikipedia.org/wiki/List_of_OEIS_sequences)
# > Natural Numbers
points = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# > Square Numbers
#points = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]
# > Prime Numbers
#points = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
# > Lucky Numbers
#points = [3, 7, 13, 31, 37, 43, 67, 73, 79, 127, 151, 163]
# > Cube Numbers
#points = [0, 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728]
# > Fermat Numbers (n >= 0)
#points = [3, 5, 17, 257, 65537, 4294967297, 18446744073709551617]
# > Semiprime Numbers
#points = [4, 6, 9, 10, 14, 15, 21, 22, 25, 26, 33, 34]
# > Magic Numbers
#points = [2, 8, 20, 28, 50, 82, 126]

# > n-Queens Fundamental Sequence (n >= 4)
#points = [1, 2, 1, 6, 12, 46, 92, 341, 1787, 9233, 45752, 285053, 1846955,
#          11977939, 83263591, 621012754, 4878666808, 39333324973, 336376244042,
#          3029242658210, 28439272956934, 275986683743434, 2789712466510289,
#          29363495934315694]
# > n-Queens Total Solutions Sequence (n >= 4)
#points = [2, 10, 4, 40, 92, 352, 724, 2680, 14200, 73712, 365596, 2279184,
#          14772512, 95815104, 666090624, 4968057848, 39029188884,
#          314666222712, 2691008701644, 24233937684440, 227514171973736,
#          2207893435808352, 22317699616364044, 234907967154122528]


# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1


pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-1, 1))
pset.renameArguments(ARG0='x')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalSymbReg(individual, points):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function : x**4 + x**3 + x**2 + x
    sqerrors = ((func(n) - val) ** 2 for n, val in enumerate(points, start=4))
    return math.fsum(sqerrors) / len(points),


toolbox.register("evaluate", evalSymbReg, points=points)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"),
                                        max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"),
                                          max_value=17))


def main():
    random.seed(318)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 100, stats=mstats,
                                   halloffame=hof, verbose=True)

    # Dump out the best individual
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=hof.items[0])
    # Print out all values of n
    #
    values = [func(n) for n,_ in enumerate(points, start=4)]
    print(", ".join(map(str, values)))

# TODO: Need to print out if we've been successful or not.

    return pop, log, hof


if __name__ == "__main__":
    main()
