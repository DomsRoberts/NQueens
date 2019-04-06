import random


def create_crossover(loc_one, loc_two):
    cross_point = random.randint(0, len(loc_one))
    result = loc_one[:cross_point] + loc_two[cross_point:]
    return result


def perform_mutation(location):
    swapPosition1 = random.randint(0, len(location) - 1)
    swapPosition2 = swapPosition1;
    while (swapPosition1 == swapPosition2):
        swapPosition2 = random.randint(0, len(location) - 1)

    first_swap = min(swapPosition1, swapPosition2)
    last_swap = max(swapPosition1, swapPosition2)
    first_val = location[first_swap]
    last_val = location[last_swap]
    start = location[:first_swap] if first_swap > 0 else []
    mid = location[first_swap + 1: last_swap]
    end = location[last_swap + 1:]
    start.append(last_val)
    start.extend(mid)
    start.append(first_val)
    start.extend(end)
    #new_location = start + last_val + mid + first_val + end

    return start


def switch_positions(location, switches):
    new_location = location
    for x in range(0, switches):
        new_location = perform_mutation(new_location)

    return new_location

def create_random_location(dimensions):
    loc = []
    selections = [x for x in range(0, dimensions - 1)]
    for index in range(0, dimensions):
        select = random.randint(0, len(selections) - 1)
        item = selections[select]
        selections = selections.remove(item)
        loc.append(item)

    return loc