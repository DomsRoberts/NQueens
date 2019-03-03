import random


def create_crossover(loc_one, loc_two):
    cross_point = random.randint(0, len(loc_one))
    result = loc_one[:cross_point] + loc_two[cross_point:]
    return result


def create_random_location(dimensions):
    loc = ""
    for index in range(0, dimensions):
        val = random.randint(0, dimensions - 1)
        char = chr(ord('A') + val)
        loc = loc + char

    return loc