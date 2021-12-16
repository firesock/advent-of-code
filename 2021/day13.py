import operator

from common import problem_data

def dots(input_data):
    points = set()
    while (line := next(input_data).strip()) != "":
        x_str, y_str = line.split(",")
        x = int(x_str, base=10)
        y = int(y_str, base=10)
        points.add((x, y))
    return points


def instructions(input_data):
    commands = []
    for line in input_data:
        axis, value = line.lstrip("fold along ").split("=")
        commands.append((axis, int(value, base=10)))
    return commands


def parse_paper(filename):
    data = problem_data(filename)
    return (dots(data), instructions(data))


def fold(dots, axis, value):
    updated_dots = set()
    if axis == "y":
        for x, y in dots:
            if y > value:
                new_y = value - (y - value)
                updated_dots.add((x, new_y))
            else:
                updated_dots.add((x, y))
    elif axis == "x":
        for x, y in dots:
            if x > value:
                new_x = value - (x - value)
                updated_dots.add((new_x, y))
            else:
                updated_dots.add((x, y))

    return updated_dots

def one_instruction(paper):
    dots, instructions = paper
    return fold(dots, instructions[0][0], instructions[0][1])

print(len(one_instruction(parse_paper("day13_sample.txt"))))

def run_paper(paper):
    dots, instructions = paper

    for axis, value in instructions:
        dots = fold(dots, axis, value)

    return dots

print(len(run_paper(parse_paper("day13_sample.txt"))))

print(len(one_instruction(parse_paper("day13_problem.txt"))))

def draw_dots(dots):
    max_x = max(map(operator.itemgetter(0), dots))
    max_y = max(map(operator.itemgetter(1), dots))

    for i in range(max_y + 1):
        for j in range(max_x + 1):
            if (j, i) in dots:
                print("#", end="")
            else:
                print(".", end="")
        print()

draw_dots(run_paper(parse_paper("day13_sample.txt")))
draw_dots(run_paper(parse_paper("day13_problem.txt")))
