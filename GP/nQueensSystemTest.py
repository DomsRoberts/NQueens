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
__date__ = '28-03-2019'
__version__ = '1.0'
__copyright__ = 'http://www.apache.org/licenses/LICENSE-2.0'

#
# Main script defines
#
SCRIPTNAME = os.path.basename(sys.argv[0])
SCRIPTINFO = "{} version: {}, {}".format(SCRIPTNAME, __version__, __date__)


def main():
    '''
    System test code.
    Params:
        N/A
    Returns:
        N/A
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
