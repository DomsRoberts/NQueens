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
System Test script for the nQueens.py GP implementation.
'''

import os
import sys
import time                     # Used to time script execution.
import argparse
import operator
import math
import random
import numpy
import nQueens


__author__ = 'David Kind'
__date__ = '20-04-2019'
__version__ = '1.0'
__copyright__ = 'http://www.apache.org/licenses/LICENSE-2.0'

#
# Main script defines
#
SCRIPTNAME = os.path.basename(sys.argv[0])
SCRIPTINFO = "{} version: {}, {}".format(SCRIPTNAME, __version__, __date__)

def test_script():
    '''
    Tests the main nQueens.py  script.
    '''
    integer_sequence = [*nQueens.SEQUENCES]
    integer_sequence = integer_sequence[0]
    maximum_number_of_terms = 9
    ga_population_size = 400
    ga_number_of_generations = 60

    nQueens.main(integer_sequence,
                 maximum_number_of_terms,
                 ga_population_size,
                 ga_number_of_generations)


def test_primes():
    '''
    Tests nQueens.py script function.
    '''
    integer_sequence = [*nQueens.SEQUENCES['Prime']]
    pstart = integer_sequence[0]
    plen = len(integer_sequence[1])
    pend = pstart + plen
    for n in range(0, (pend + 1)):
        print("P{} = {}".format(n, nQueens.pprime(n)))

def test_seqsum():
    '''
    Tests nQueens.py script class seqsum() funtion.
    '''
    integer_sequence = [*nQueens.SEQUENCES['Prime']]
    sequence = "Prime"
    maxterms = 8
    psize = 300
    generations = 50
    # Initialise the random module and seed with the current time.
    # Note: uses the current time by default if left empty.
    random.seed()
    # Create our Integer Sequence object and initialise it
    isgp = nQueens.CIntegerSequenceGp(sequence, maxterms, psize, generations)
    # Configure the DEAP GP objects
    isgp.configure_primitives()
    isgp.configure_toolbox()
    isgp.set_population()
    isgp.config_statistics()
    # Have configured the object, so we're now ready to test seqsum()
    suceeded = True
    idx = isgp.start
    for n in range(100):
        isgp.n = idx + n
        if isgp.seqsum() != math.fsum(integer_sequence[1][:n]):
            suceeded = False
            break
    if suceeded:
        print("test_seqsum() successfully tested.")
    else:
        print("test_seqsum() FAILED.")

def test_seqn1():
    '''
    Tests nQueens.py script class seqsum() funtion.
    '''
    integer_sequence = [*nQueens.SEQUENCES['Prime']]
    sequence = "Prime"
    maxterms = 8
    psize = 300
    generations = 50
    # Initialise the random module and seed with the current time.
    # Note: uses the current time by default if left empty.
    random.seed()
    # Create our Integer Sequence object and initialise it
    isgp = nQueens.CIntegerSequenceGp(sequence, maxterms, psize, generations)
    # Configure the DEAP GP objects
    isgp.configure_primitives()
    isgp.configure_toolbox()
    isgp.set_population()
    isgp.config_statistics()
    # Have configured the object, so we're now ready to test seqsum()
    suceeded = True
    for isgp.n in range(isgp.start, len(integer_sequence[1])):
        result = isgp.seq_n1()
        expected = float(integer_sequence[1][isgp.n - isgp.start - 1])
        if isgp.n == isgp.start:
            if result != 0:
                print("Should have returned zero.")
                suceeded = False
                break
        elif result != expected:
            print("Got {}, but expected {}".format(result, expected))
            suceeded = False
            break
    if suceeded:
        print("test_seqn1() successfully tested.")
    else:
        print("test_seqn1() FAILED.")


def main():
    '''
    System test code.
    Params:
        N/A
    Returns:
        N/A
    '''
#    test_script()
#    test_primes()
#    test_seqsum()
    test_seqn1()


if __name__ == "__main__":
    start = time.time()        # Used to time script execution.
    PARSER = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('--version', action='version', version=SCRIPTINFO)
    PARSER.add_argument('--timer', '-t',
                        help='Script execution time.',
                        action='store_true')
    # Get the arguments dictionary, where arguments are the keys.
    ARGS = vars(PARSER.parse_args())
    # Execute the system test.
    main()
    # Are we on the timer?
    if ARGS['timer']:
        print("\nScript execution time:", time.time() - start, "seconds")

# EOF
