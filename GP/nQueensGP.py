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
'''

__author__ = 'David Kind'
__date__ = '14-03-2019'
__version__ = '1.0'
__copyright__ = 'Copyright (c) 2019'


import os
import sys
import argparse
import time                     # Use to time script execution.
import random
from deap import creator, base, tools, algorithms


# Main script defines
SCRIPTNAME = os.path.basename(sys.argv[0])
SCRIPTINFO = "{} version: {}, {}".format(SCRIPTNAME, __version__, __date__)


def main():
    '''Main function'''
    print('Running main function')


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

    # Did user want to time the script?
    if ARGS['timer']:
        print("Script execution time:", time.time() - START, "seconds")

# EOF
