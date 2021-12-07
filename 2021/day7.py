import math

from common import problem_data

def crabs(input_data):
    return [int(c, base=10) for c in next(input_data).split(",")]

def fuel_cost(crabs, position):
    cost = 0
    for crab in crabs:
        cost += abs(crab - position)
    return cost

def find_lowest_cost(crabs):
    max_crab = max(crabs)

    lowest_cost = math.inf
    for i in range(max_crab + 1):
        cost = fuel_cost(crabs, i)

        if cost < lowest_cost:
            lowest_cost = cost

    return lowest_cost

print(find_lowest_cost(crabs(problem_data("day7_sample.txt"))))
print(find_lowest_cost(crabs(problem_data("day7_problem.txt"))))

def step_costs(max_count):
    costs = [0]
    for i in range(1, max_count + 1):
        costs.append(i + costs[-1])
    return costs

def fuel_rising_cost(crabs, position, costs):
    cost = 0
    for crab in crabs:
        cost += costs[abs(crab - position)]
    return cost

def find_lowest_rising_cost(crabs):
    max_crab = max(crabs)
    costs = step_costs(max_crab)

    lowest_cost = math.inf
    for i in range(max_crab + 1):
        cost = fuel_rising_cost(crabs, i, costs)

        if cost < lowest_cost:
            lowest_cost = cost

    return lowest_cost

print(find_lowest_rising_cost(crabs(problem_data("day7_sample.txt"))))
print(find_lowest_rising_cost(crabs(problem_data("day7_problem.txt"))))
