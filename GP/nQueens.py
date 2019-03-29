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

Shell execution example: py -3 nQueens.py Natural 8 300 50
Running the GP:
    > against the Natural Number sequence;
    > with a maximum number of 8 terms from the sequence to check;
    > with a population of 300;
    > over 50 generations

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

__author__ = 'David Kind'
__date__ = '28-03-2019'
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

# TODO: Is there an optimum number of values required to learn the integer
#  sequence? Test min/max???

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
            # Natural numbers; n=1 (https://oeis.org/A000027)
            "Natural":[1,
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]],
            # Square numbers; n=0 (https://oeis.org/A000290)
            "Square":[0,
                      [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]],
            # Prime numbers; n=1 (https://oeis.org/A000040)
            "Prime":[1,
                     [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]],
            # Lucky numbers; n=1 (https://oeis.org/A000959)
            "Lucky":[1,
                     [1, 3, 7, 13, 31, 37, 43, 67, 73, 79, 127, 151, 163]],
            # Cube numbers; n=0 (https://oeis.org/A000578)
            "Cube":[0,
                    [0, 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728]],
            # Fermat numbers; n=0 (https://oeis.org/A000215)
            "Fermat":[0,
                      [3, 5, 17, 257, 65537, 4294967297, 18446744073709551617]],
            # Semiprimes or biprimes; n=1 (https://oeis.org/A001358)
            "Semiprime":[1,
                         [4, 6, 9, 10, 14, 15, 21, 22, 25, 26, 33, 34]],
            # Magic numbers; n=1 (https://oeis.org/A018226)
            "Magic":[1,
                     [2, 8, 20, 28, 50, 82, 126]],
            # n-Queens fundamental numbers; n=1 (https://oeis.org/A002562)
            "nQueensFundamental":[1,
                                  [1, 0, 0, 1, 2, 1, 6, 12, 46, 92, 341, 1787,
                                  9233, 45752, 285053, 1846955, 11977939,
                                  83263591, 621012754, 4878666808,
                                  39333324973, 336376244042,
                                  3029242658210, 28439272956934,
                                  275986683743434, 2789712466510289,
                                  29363495934315694]],
            # n-Queens fundamental numbers; n=0 (https://oeis.org/A000170)
            "nQueensAll":[0,
                          [1, 1, 0, 0, 2, 10, 4, 40, 92, 352, 724, 2680, 14200,
                          73712, 365596, 2279184, 14772512, 95815104,
                          666090624, 4968057848, 39029188884, 314666222712,
                          2691008701644, 24233937684440, 227514171973736,
                          2207893435808352, 22317699616364044,
                          234907967154122528]]
            }

# Define new functions
def protected_divide(numerator, denominator):
    '''
    Protected division; protect against potential divide by zero errors.
    Params:
        numerator   - individual object; individual to be tested.
        denominator - integer number list; terms to match.
	Returns:
    	Division result or 0 if denominator is 0.
    '''
    retval = 0
    if denominator:
        retval = numerator / denominator
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
        self.pset = gp.PrimitiveSet("MAIN", 1)
        # Can now add the primitive operators
        self.pset.addPrimitive(operator.add, 2)
        self.pset.addPrimitive(operator.sub, 2)
        self.pset.addPrimitive(operator.mul, 2)
        self.pset.addPrimitive(protected_divide, 2)
        self.pset.addPrimitive(operator.neg, 1)
        self.pset.addPrimitive(math.cos, 1)
        self.pset.addPrimitive(math.sin, 1)
# TODO: More examples: will need to define the handling conditional function
# pset.addPrimitive(if_then_else, 3)
# pset.addTerminal(1)
# pset.addTerminal(0)
        # Ref: DEAP 1.2.2 Documentation on Genetic Programming
        # An ephemeral constant is a terminal encapsulating a value that is
        # generated from a given function at run time. The ephemeral constant
        # value is determined when it is inserted in the tree and never
        # changes unless it is replaced by another ephemeral constant.
        self.pset.addEphemeralConstant("rand101", lambda: random.randint(-1, 1))
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
        sqerrors = ((func(n) - val) ** 2 for n, val in enumerate(points, start=self.start))
        return math.fsum(sqerrors) / len(points),

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

    def execute_gp(self):
        '''
        Execute the DEAP GP according to the specified configuration.
        Running the algorithm results in it returning an optimised population
        and the statistics log for each generation.
        Params:
            N/A
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
        else:
            self.rlist = None
            self.expr = None
        self.pop = pop
        self.log = log

    def show_results(self):
        '''
        Display the results of executing the DEAP GP object; best individual
        is displayed.
        Params:
            N/A
        Returns:
            N/A
        '''
        if self.rlist:
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
#            nodes, edges, labels = gp.graph(expr)
            if sys.platform == 'linux' or sys.platform == 'linux2':
                print("Running on Linux OS.")
                ### Graphviz Section ###
#               import pygraphviz as pgv

#               g = pgv.AGraph()
#               g.add_nodes_from(nodes)
#               g.add_edges_from(edges)
#               g.layout(prog="dot")

#               for i in nodes:
#                   n = g.get_node(i)
#                   n.attr["label"] = labels[i]

#               g.draw("tree.pdf")
###########################################################
#               import matplotlib.pyplot as plt
#               import networkx as nx

#               g = nx.Graph()
#               g.add_nodes_from(nodes)
#               g.add_edges_from(edges)
#               pos = nx.graphviz_layout(g, prog="dot")

#               nx.draw_networkx_nodes(g, pos)
#               nx.draw_networkx_edges(g, pos)
#               nx.draw_networkx_labels(g, pos, labels)
#               plt.show()
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


def main(sequence, maxterms, psize, generations):
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
    isgp.execute_gp()

    # Show the results
    isgp.show_results()
    # Save the results
    results_filename = "results-{}_{}_{}_{}.txt" \
                       .format(sequence, maxterms, psize, generations)
    isgp.save_results(results_filename)


if __name__ == "__main__":
    start = time.time()        # Used to time script execution.
    PARSER = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('sequence', nargs=1, help='Integer number sequence.')
    PARSER.add_argument('maxterms', nargs=1, help='Maximum number of terms.')
    PARSER.add_argument('psize', nargs=1, help='Population size.')
    PARSER.add_argument('generations', nargs=1, help='Number of generations.')
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
        main(seq, mterms, population_size, gens)

    # Are we on the timer?
    if ARGS['timer']:
        print("\nScript execution time:", time.time() - start, "seconds")

# EOF
