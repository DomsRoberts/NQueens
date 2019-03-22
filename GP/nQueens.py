#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

'''
Genetic Programming (GP) algorithm to evolve an equation for calculating the
fundamental number of solutions to n for the n-Queens Problem.
The following libraries need to be installed:
py -3 -m pip install scoop
py -3 -m pip install numpy
py -3 -m pip install matplotlib
py -3 -m pip install version_information
py -3 -m pip install networkx
'''

__author__ = 'David Kind'
__date__ = '14-03-2019'
__version__ = '1.0'
__copyright__ = 'Copyright (c) 2019'


import os
import sys
import argparse
import time                     # Use to time script execution.
import numpy
import random
import operator
import networkx as nx
import matplotlib.pyplot as plt
from deap import creator, base, tools, algorithms, gp


# Main script defines
SCRIPTNAME = os.path.basename(sys.argv[0])
SCRIPTINFO = "{} version: {}, {}".format(SCRIPTNAME, __version__, __date__)

# Initialize Parity problem input and output matrices
PARITY_FANIN_M = 6
PARITY_SIZE_M = 2 ** PARITY_FANIN_M

inputs = [None] * PARITY_SIZE_M
outputs = [None] * PARITY_SIZE_M

for i in range(PARITY_SIZE_M):
    inputs[i] = [None] * PARITY_FANIN_M
    value = i
    dividor = PARITY_SIZE_M
    parity = 1
    for j in range(PARITY_FANIN_M):
        dividor /= 2
        if value >= dividor:
            inputs[i][j] = 1
            parity = int(not parity)
            value -= dividor
        else:
            inputs[i][j] = 0
    outputs[i] = parity

pset = gp.PrimitiveSet("MAIN", PARITY_FANIN_M, "IN")
pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.xor, 2)
pset.addPrimitive(operator.not_, 1)
pset.addTerminal(1)
pset.addTerminal(0)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=3, max_=5)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalParity(individual):
    func = toolbox.compile(expr=individual)
    return sum(func(*in_) == out for in_, out in zip(inputs, outputs)),

toolbox.register("evaluate", evalParity)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    '''Main function'''
    print('Running main function')
    random.seed(21)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 40, stats, halloffame=hof)

    return pop, stats, hof


if __name__ == '__main__':
    START = time.time()        # Used to time script execution.
    PARSER = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('--version', action='version', version=SCRIPTINFO)
    PARSER.add_argument('--timer', '-t',
                        help='Script execution time.',
                        action='store_true')
    # Get the arguments dictionary, where arguments are the keys.
    ARGS = vars(PARSER.parse_args())

    # Start application
    main()

    # Display the individual
#    expr = toolbox.individual()
#    nodes, edges, labels = gp.graph(expr)
#    g = nx.Graph()
#    g.add_nodes_from(nodes)
#    g.add_edges_from(edges)
#    pos = nx.graphviz_layout(g, prog="dot")

#    nx.draw_networkx_nodes(g, pos)
#    nx.draw_networkx_edges(g, pos)
#    nx.draw_networkx_labels(g, pos, labels)
#    plt.show()

# TODO: DEBUG only: remove me:
    expr = toolbox.individual()
    print(expr)
# TODO: DEBUG only: remove me:

    # Did user want to time the script?
    if ARGS['timer']:
        print("Script execution time:", time.time() - START, "seconds")

# EOF
