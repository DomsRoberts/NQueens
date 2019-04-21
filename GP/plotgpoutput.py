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
Simple script to draw a plot of the GP results.
'''

import os
import sys
import time                     # Used to time script execution.
import argparse
import re
# TODO: remove me unused imports...
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
__date__ = '20-04-2019'
__version__ = '1.0'
__copyright__ = 'http://www.apache.org/licenses/LICENSE-2.0'

#
# Main script defines
#
SCRIPTNAME = os.path.basename(sys.argv[0])
SCRIPTINFO = "{} version: {}, {}".format(SCRIPTNAME, __version__, __date__)


def main(fname):
    '''
    Reads in the specifed GP result file extracting the generations, minimum
    fitness value and average tree size. These are then plotted on a graph.
    Params:
        file - string of the GP results filename.
    Returns:
        -1: failed, 0: succeeded
    '''
    # Attempt to open the file and read in the contents.
    # Process the entire file for ease and speed.
    with open(fname, "r") as fin:
        # read in the whole file in one go.
        contents = fin.read()

    # Process the file a line at a time; looked at regex, but became really
    # complicated when sifting through all the floats.
    generation = []
    minfitness = []
    avgindsize = []
    start_condition = False
    for line in contents.splitlines():
        # split the line according to spaces in between data
        line = re.split("\s+", line)
#        print(line)
        if start_condition:
            # Look for the end of the data.
            if len(line) < 10:
                # Nothing more to process; exit loop
                break
            generation.append(float(line[0]))
            minfitness.append(float(line[4]))
            avgindsize.append(float(line[6]))
        if line[0] == 'gen':
            start_condition = True

    # Now have the required data as separate lists.
    # Plot the result using matplotlib plotting both sets of data on the same
    # plot using the generations as the common X-axis.
#    print(generation)
#    print(minfitness)
#    print(avgindsize)
#    plt.xlabel('Generation')
#    plt.ylabel('Min.Fitness')
#    plt.title('GP Fitness Evolution')
    genmax = max(generation)
    fitmax = max(minfitness)
    if fitmax % 1000 != 0:
        fitmax = (fitmax + 1000 - (fitmax % 1000))
#    print(genmax, fitmax)
#    plt.plot(generation, minfitness, color='r')
#    plt.plot(generation, avgindsize, color='b')
#    plt.axis([0, genmax, 0, fitmax])

#    plt.show()

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Generations')
    ax1.set_ylabel('Min-fitness', color=color)
    ax1.plot(generation, minfitness, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Avg.Ind.Size', color=color)
    # with ax1
    ax2.plot(generation, avgindsize, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plttitle = fname.split('.')
    plttitle = plttitle[0].split('-')
    plttitle = plttitle[1]
    # Remove the filename extension
    gtitle = os.path.splitext(fname)[0]
    gtitle = gtitle.split('-')
    gtitle = gtitle[1]
    fname = 'plot-' + gtitle
    plt.title(gtitle, None, 'center', None)
    plt.grid(True)

#    print('#2 Backend:', plt.get_backend())
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    plt.savefig(fname + '.png')
#    plt.show()


if __name__ == "__main__":
    start = time.time()        # Used to time script execution.
    PARSER = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('file', nargs=1, help='Results file to process.')
    PARSER.add_argument('--version', action='version', version=SCRIPTINFO)

    # Get the arguments dictionary, where arguments are the keys.
    ARGS = vars(PARSER.parse_args())

    # Start up the application
    main(ARGS['file'][0])

# EOF
