from common import problem_data

def new_location(course):
    horizontal = 0
    depth = 0
    for instruction in course:
        direction, mstr = instruction.split()
        magnitude = int(mstr, base=10)
        if direction == "forward":
            horizontal += magnitude
        elif direction == "down":
            depth += magnitude
        elif direction == "up":
            depth -= magnitude

    return horizontal * depth

print(new_location(problem_data("day2_sample.txt")))
print(new_location(problem_data("day2_problem.txt")))


def new_location_with_aim(course):
    horizontal = 0
    depth = 0
    aim = 0
    for instruction in course:
        direction, mstr = instruction.split()
        magnitude = int(mstr, base=10)
        if direction == "forward":
            horizontal += magnitude
            depth += (aim * magnitude)
        elif direction == "down":
            aim += magnitude
        elif direction == "up":
            aim -= magnitude

    return horizontal * depth


print(new_location_with_aim(problem_data("day2_sample.txt")))
print(new_location_with_aim(problem_data("day2_problem.txt")))
