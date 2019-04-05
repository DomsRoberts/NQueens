#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019 David Kind
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
#

'''
The n-Queens problem is an age old problem first published by Max Bezzel in 1848
who first wrote about placing 8 Queens on an 8 x 8 chess board so that none of
the Queens were able to attack each other. This problem was later extended to
n-Queens on an n x n chessboard by Franz Nauck in 1850. While the concept may
sound simple, the problem is prohibitively computationally expensive as n
increases in size; where n >= 1 integer. The number of solutions to the n-Queens
problem, fundamental and all solutions, are integer sequences. This Genetic
Program attempts to solve the n-Queens integer sequences by inductively creating
an equation using the tree method.

Shell execution examples:
    py -3 nQueens.py Natural 8 300 50
Running the GP:
    > against the Natural Number sequence;
    > with a maximum number of 8 terms from the sequence to check;
    > with a population of 300;
    > over 50 generations

    py -3 nQueens.py Prime 8 300 50 --round
Running the GP:
    > against the Prime Number sequence;
    > with a maximum number of 8 terms from the sequence to check;
    > with a population of 300;
    > over 50 generations
    > rounding the resultant number sequence

Note: this script has been developed to use Python 3.
'''

import os
import sys
import time                     # Used to time script execution.
import argparse
import operator
import math
import random
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
# libraries required for the tree diagrams (Linux)
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

__author__ = 'David Kind'
__date__ = '05-04-2019'
__version__ = '1.0'
__copyright__ = 'http://www.apache.org/licenses/LICENSE-2.0'

#
# Main script defines
#
SCRIPTNAME = os.path.basename(sys.argv[0])
SCRIPTINFO = "{} version: {}, {}".format(SCRIPTNAME, __version__, __date__)

# GP specific definitions
MUTATION_RATE = 0.1     # Probability of mutating an individual (%)
MATING_RATE = 0.5       # Probability of mating two individuals (%)

# Defined Integer Sequences (Test cases)
# Note these sequences are usually infinite so a limited number only have been
# incorporated for test purposes. The number of the values for each sequence
# can vary as the script will automatically adapt to the length.
# Ref: Wikipedia List of OEIS Sequences
# (https://en.wikipedia.org/wiki/List_of_OEIS_sequences)

# Dictionary format:
#       key:    Number sequence name string
#       value:
#               [0]: OEIS Offset 'n'
#               [1]: Number sequence list of varying length
#  Note: Have to watch that numbers don't get too large and overflow the
#  variable type size.
SEQUENCES = {
            # Linear Integer Sequences
            # Natural numbers; n=1 (https://oeis.org/A000027)
            "Natural": [1,
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                       17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                       31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
                       45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
                       59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72,
                       73, 74, 75, 76, 77]],
            # Even numbers; n=0 (https://oeis.org/A005843)
            "Even": [0,
                    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30,
                    32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60,
                    62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90,
                    92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116,
                    118, 120]],
            # Odd numbers; n=0 (https://oeis.org/A005408)
            "Odd": [0,
                   [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29,
                   31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57,
                   59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85,
                   87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111,
                   113, 115, 117, 119, 121, 123, 125, 127, 129, 131]],
            # Non-linear Integer Sequences
            # Square numbers; n=0 (https://oeis.org/A000290)
            "Square": [0,
                      [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169,
                      196, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576,
                      625, 676, 729, 784, 841, 900, 961, 1024, 1089, 1156,
                      1225, 1296, 1369, 1444, 1521, 1600, 1681, 1764, 1849,
                      1936, 2025, 2116, 2209, 2304, 2401, 2500]],
            # Cube numbers; n=0 (https://oeis.org/A000578)
            "Cube": [0,
                    [0, 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728,
                    2197, 2744, 3375, 4096, 4913, 5832, 6859, 8000, 9261, 10648,
                    12167, 13824, 15625, 17576, 19683, 21952, 24389, 27000,
                    29791, 32768, 35937, 39304, 42875, 46656, 50653, 54872,
                    59319, 64000]],
            # Prime numbers; n=1 (https://oeis.org/A000040)
            "Prime": [1,
                     [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                     53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
                     109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
                     179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
                     239, 241, 251, 257, 263, 269, 271]],
            # Lucky numbers; n=1 (https://oeis.org/A000959)
            "Lucky": [1,
                     [1, 3, 7, 9, 13, 15, 21, 25, 31, 33, 37, 43, 49, 51, 63,
                     67, 69, 73, 75, 79, 87, 93, 99, 105, 111, 115, 127, 129,
                     133, 135, 141, 151, 159, 163, 169, 171, 189, 193, 195, 201,
                     205, 211, 219, 223, 231, 235, 237, 241, 259, 261, 267,
                     273, 283, 285, 289, 297, 303]],
            # Fermat numbers; n=0 (https://oeis.org/A000215)
            "Fermat": [0,
                      [3, 5, 17, 257, 65537, 4294967297, 18446744073709551617]],
            # Semiprimes or biprimes; n=1 (https://oeis.org/A001358)
            "Semiprime": [1,
                         [4, 6, 9, 10, 14, 15, 21, 22, 25, 26, 33, 34, 35, 38,
                         39, 46, 49, 51, 55, 57, 58, 62, 65, 69, 74, 77, 82,
                         85, 86, 87, 91, 93, 94, 95, 106, 111, 115, 118, 119,
                         121, 122, 123, 129, 133, 134, 141, 142, 143, 145,
                         146, 155, 158, 159, 161, 166, 169, 177, 178, 183, 185,
                         187]],
            # Magic numbers; n=1 (https://oeis.org/A018226)
            "Magic": [1,
                     [2, 8, 20, 28, 50, 82, 126]],
            # n-Queens fundamental numbers; n=1 (https://oeis.org/A002562)
            "nQueensFundamental": [1,
                                  [1, 0, 0, 1, 2, 1, 6, 12, 46, 92, 341, 1787,
                                  9233, 45752, 285053, 1846955, 11977939,
                                  83263591, 621012754, 4878666808,
                                  39333324973, 336376244042,
                                  3029242658210, 28439272956934,
                                  275986683743434, 2789712466510289,
                                  29363495934315694]],
            # n-Queens fundamental numbers; n=0 (https://oeis.org/A000170)
            "nQueensAll": [0,
                          [1, 1, 0, 0, 2, 10, 4, 40, 92, 352, 724, 2680, 14200,
                          73712, 365596, 2279184, 14772512, 95815104,
                          666090624, 4968057848, 39029188884, 314666222712,
                          2691008701644, 24233937684440, 227514171973736,
                          2207893435808352, 22317699616364044,
                          234907967154122528]]
            }

# Define new functions
def pdiv(numerator, denominator):
    '''
    Protected division; protect against potential divide by zero errors.
    Params:
        numerator   - individual object; individual to be tested.
        denominator - integer number list; terms to match.
	Returns:
    	Division result or 0 if denominator is 0.
    '''
    if denominator:
        retval = numerator / denominator
    else:
        retval = 0
    return retval

def pfac(value):
    '''
    Protected division; protect against potential divide by zero errors.
    Params:
        numerator   - individual object; individual to be tested.
        denominator - integer number list; terms to match.
	Returns:
    	Division result or 0 if denominator is 0.
    '''
    if value == int and value < 50 and value > 0:
        retval = math.factorial(value)
    else:
        retval = 0
    return retval

class CIntegerSequenceGp:
    '''
    Integer sequence Genetic Program using the DEAP module library.
    '''
    def __init__(self, intseq, mterms, popsize, gens):
        # Assign the Integer Sequence name, n start value and the associated
        # list contents from the passed in intseq name string.
        self.sname = intseq
        self.start = SEQUENCES[self.sname][0]
        self.slist = SEQUENCES[self.sname][1]
        self.maxterms = mterms
        self.psize = popsize
        self.generations = gens

    def configure_primitives(self):
        '''
        Initialise the primitive set with the required mathematical operations
        We only have one input: ARG0, which represents 'n'. The number of
        inputs is specified by the second argument in the PrimitiveSet.
        Params:
            N/A
        Returns:
            N/A
        '''
# TODO: Example script adf_symbreg.py shows how you can specify different
#       primitive sets and then cycle through them for test purposes.
        self.pset = gp.PrimitiveSetTyped("MAIN", [int], int)

        # Can now add the primitive operators
        self.pset.addPrimitive(operator.add, [float, int], float)
        self.pset.addPrimitive(operator.sub, [float, int], float)
        self.pset.addPrimitive(operator.mul, [float, int], float)
        self.pset.addPrimitive(pdiv, [float, int], float)
        self.pset.addPrimitive(pfac, [int], int)

        self.pset.addPrimitive(operator.abs, [float], float)
        self.pset.addPrimitive(operator.neg, [float], float)
        self.pset.addPrimitive(math.cos, [float], float)
        self.pset.addPrimitive(math.sin, [float], float)
        self.pset.addPrimitive(round, [float], int)

        # Ref: DEAP 1.2.2 Documentation on Genetic Programming
        # An ephemeral constant is a terminal encapsulating a value that is
        # generated from a given function at run time. The ephemeral constant
        # value is determined when it is inserted in the tree and never
        # changes unless it is replaced by another ephemeral constant.
        self.pset.addEphemeralConstant("rand101",
                                       lambda: random.randint(-1, 1), int)
        self.pset.addTerminal(math.pi, float, "pi")
        # We only have one input argument 'n' indexing the current integer in
        # the sequence.
        self.pset.renameArguments(ARG0='n')

    def configure_toolbox(self):
        '''
        Initialise the fitness optimization method and the toolbox.
        Params:
            N/A
        Returns:
            N/A
        '''
        # Configure the optimization to be for a minima
        # This is done by creating a new class based on Fitness, but with a
        # range from -1.0 to zero. We can then create a new Individual class
        # based on the PrimitiveTree and inheriting from the FitnessMin class.
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)
        # Can now create the toolbox which contains everything required to run
        # our GP.
        self.toolbox = base.Toolbox()
        self.toolbox.register("expr",
                              gp.genHalfAndHalf, pset=self.pset, min_=1, max_=2)
        self.toolbox.register("individual",
                              tools.initIterate, creator.Individual,
                              self.toolbox.expr)
        self.toolbox.register("population",
                              tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("compile", gp.compile, pset=self.pset)
        # Limit number of points in the list to command line specified value.
        # This is done so that we can characterise the GP performance depending
        # on list length and also to enable us to reduce overall processing
        # time by not processing all the terms. The final solution should be
        # evaluated against all the terms in the sequence list.
        points = self.slist[:self.maxterms]
        self.toolbox.register("evaluate", self.eval_sequence, points=points)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", gp.mutUniform,
                              expr=self.toolbox.expr_mut, pset=self.pset)

        self.toolbox.decorate("mate",
                              gp.staticLimit(key=operator.attrgetter("height"),
                              max_value=17))
        self.toolbox.decorate("mutate",
                              gp.staticLimit(key=operator.attrgetter("height"),
                              max_value=17))

    def eval_sequence(self, individual, points):
        '''
        Evaluate the individual's tree function on the values of 'n' and
        report the mean squared error of doing so.
        Params:
            individual  - individual object; individual to be tested.
            points      - integer number list; terms to match.
        Returns:
            Sum of the mean squared error to the required values of 'n'.
        '''
        # Transform the tree expression in a callable function
        func = self.toolbox.compile(expr=individual)
        # Evaluate the mean squared error between the expression
	    # and the recorded Integer Sequence values.
        size = len(points)
        try:
            sqerrors = ((func(n) - val) ** 2 for n, val in enumerate(points, start=self.start))
            sqerrors = math.fsum(sqerrors) / size
        except Exception as ex:
            sqerrors = 10.0
        return sqerrors,

    def set_population(self):
        '''
        Set up the DEAP toolbox population size and create the hall of fame
        object so that the best performing individuals can be recorded.
        Params:
            N/A
        Returns:
            N/A
        '''
        self.pop = self.toolbox.population(n=self.psize)
        self.hof = tools.HallOfFame(1)
        self.log = None
        self.rlist = None

    def config_statistics(self):
        '''
        Registers the statistics object and the required metrics.
        Params:
            N/A
        Returns:
            N/A
        '''
        stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(len)
        self.mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
        self.mstats.register("avg", numpy.mean)
        self.mstats.register("std", numpy.std)
        self.mstats.register("min", numpy.min)
        self.mstats.register("max", numpy.max)

    def execute_gp(self, rounded=False):
        '''
        Execute the DEAP GP according to the specified configuration.
        Running the algorithm results in it returning an optimised population
        and the statistics log for each generation.
        Params:
            rounded - boolean flag; True=round resultant numbers
        Returns:
            N/A
        '''
        pop, log = algorithms.eaSimple(self.pop, self.toolbox,
                                       MATING_RATE, MUTATION_RATE,
                                       self.generations,
                                       stats=self.mstats,
                                       halloffame=self.hof,
                                       verbose=True)
# TODO: NEED TO INVESTIGATE THESE OTHER METHODS...
#        pop, log = gp.harm(pop, toolbox,
#                           MATING_RATE, MUTATION_RATE,
#                           self.generations,
#                           alpha=0.05, beta=10,
#                           gamma=0.25, rho=0.9,
#                           stats=self.mstats,
#                           halloffame=self.hof,
#                           verbose=True)
        # Was the DEAP GP successful?
        if self.hof.items:
            # Transform the tree expression in a callable function
            self.expr = self.hof.items[0]
            func = self.toolbox.compile(expr=self.expr)
            self.rlist = [func(n) for n, _ in enumerate(self.slist,
                                                        start=self.start)]
            # Optional rounding of values
            if rounded:
                self.rlist = [round(val) for val in self.rlist]
        else:
            self.rlist = None
            self.expr = None
        self.pop = pop
        self.log = log

    def show_results(self, gtitle):
        '''
        Display the results of executing the DEAP GP object; best individual
        is displayed.
        Params:
            gtitle - string of the graph title.
        Returns:
            N/A
        '''
        if self.rlist:
            # Show the squence required
            result = ", ".join(map(str, self.slist))
            print("\nRequired sequence: {}".format(result))
            # Show the resultant integer sequence
            result = ", ".join(map(str, self.rlist))
            print("\nCalculated result: {}".format(result))
            # Let the user know how it went.
            if self.rlist == self.slist:
                print("Successfully calculated the Integer Sequence.")
            else:
                print("Unsuccessfull in calculating the Integer Sequence.")
            # Display the individual
            print('\nBest individual : ', self.expr)
            # Display the resultant equation from the best individual
            tree = gp.PrimitiveTree(self.expr)
            str(tree)

# TODO: Display the best individual => graph and equation.
# TODO: Need to print out if we've been successful or not.
# TODO: Need to dump out GP Tree of the HOF (Hall Of Fame)
### TODO: Get this code up and running again; Windows / Linux check?!
            if sys.platform == 'linux' or sys.platform == 'linux2':
                print("Running on Linux OS.")
                nodes, edges, labels = gp.graph(self.expr)
                # Create tree diagram
                g = nx.Graph()
                g.add_nodes_from(nodes)
                g.add_edges_from(edges)
                pos = graphviz_layout(g, prog="dot")

                nx.draw_networkx_nodes(g, pos)
                nx.draw_networkx_edges(g, pos)
                nx.draw_networkx_labels(g, pos, labels)

                # Remove the filename extension
                gtitle = os.path.splitext(gtitle)[0]
                plt.title(gtitle, None, 'center', None)
                plt.savefig(gtitle + '.png')
                #                plt.show()
            else:
                print("Graphical output only available on Linux.")
        else:
            print("\nError: hof variable is emtpy.")

    def save_results(self, fname):
        '''
        Save the results of running the DEAP GP to a text file.
        Params:
            fname - string of the filename.
        Returns:
            N/A
        '''
        if self.rlist:
            print("Writing results file: {}".format(fname))
            with open(fname, "w") as fout:
                fout.writelines(str(self.log))
                best = "\n" + "-" * 80 + "\n"
                best += "\nBest individual:"
                seqstr = ", ".join(map(str, self.slist))
                best += "\nRequired sequence: {}".format(seqstr)
                seqstr = ", ".join(map(str, self.rlist))
                best += "\nActual sequence:   {}".format(seqstr)
                best += "\n\n"
                # Display the resultant equation from the best individual
                tree = gp.PrimitiveTree(self.expr)
                best += "\nBest algorithm: {}".format(str(tree))
                # Report whether the individual is a success or not.
                if self.slist == self.rlist:
                    best += "\n\nSuccess!"
                else:
                    best += "\n\nFailed!"
                fout.writelines(best)
        else:
            print("No results available to write to file.")


def main(sequence, maxterms, psize, generations, rounded):
    '''
    Execute the DEAP GP on the specified Integer Sequence for the specified
    population size and for the specified number of generations.
    Params:
        sequence    - string key to SEQUENCE dictionary; Integer Sequence Key.
        maxterms    - max integer number; terms to match from the sequence.
        psize       - integer number; GP population size.
        generations - integer number; number of generations to process.
    Returns:
        N/A
    '''
    # Initialise the random module and seed with the current time.
    # Note: uses the current time by default if left empty.
    random.seed()

    # Create our Integer Sequence object and initialise it
    isgp = CIntegerSequenceGp(sequence, maxterms, psize, generations)

    # Configure the DEAP GP objects
    isgp.configure_primitives()
    isgp.configure_toolbox()
    isgp.set_population()
    isgp.config_statistics()

    # Now run the Genetic Program code
    isgp.execute_gp(rounded)

    results_filename = "results-{}_{}_{}_{}.txt" \
                       .format(sequence, maxterms, psize, generations)
    # Show the results
    isgp.show_results(results_filename)
    # Save the results
    isgp.save_results(results_filename)

    # Clean up the object
    del(isgp)


if __name__ == "__main__":
    start = time.time()        # Used to time script execution.
    PARSER = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('sequence', nargs=1, help='Integer number sequence.')
    PARSER.add_argument('maxterms', nargs=1, help='Maximum number of terms.')
    PARSER.add_argument('psize', nargs=1, help='Population size.')
    PARSER.add_argument('generations', nargs=1, help='Number of generations.')
    PARSER.add_argument('--round', action='store_true',
                        help='Rounds the resultant sequence.')
    PARSER.add_argument('--version', action='version', version=SCRIPTINFO)
    PARSER.add_argument('--timer', '-t',
                        help='Script execution time.',
                        action='store_true')
    # Get the arguments dictionary, where arguments are the keys.
    ARGS = vars(PARSER.parse_args())

    params_ok = True
    # Check the user input for the chosen Integer Sequence
    seq = ARGS['sequence'][0]
    if not seq in SEQUENCES.keys():
        print("\nError: '{}' not a valid integer sequence.".format(seq))
        print("\nValid Integer sequences are:")
        print(", ".join(SEQUENCES.keys()))
        params_ok = False
    # Make sure the maximum number of terms to test for is an integer value.
    # Assuming it requires more than one term to determine the integer sequence.
    mterms = int(ARGS['maxterms'][0])
    if mterms < 2:
        print("\nError: maxterms must be greater than 1.")
        params_ok = False
    # Make sure the population size is an integer value and assuming the size
    # is greater than 10.
    population_size = int(ARGS['psize'][0])
    if population_size < 10:
        print("\nError: psize must be greater than 9.")
        params_ok = False
    # Make sure the generations parameter is an integer value and assuming the
    # size is greater than 10.
    gens = int(ARGS['generations'][0])
    if gens < 10:
        print("\nError: generations must be greater than 9.")
        params_ok = False

    # Start up the application
    if params_ok:
        main(seq, mterms, population_size, gens, ARGS['round'])

    # Are we on the timer?
    if ARGS['timer']:
        print("\nScript execution time:", time.time() - start, "seconds")

# EOF
