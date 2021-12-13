import os.path


def ordered_intmap(filename):
    for i, line in enumerate(problem_data(filename)):
        for j, char in enumerate(line):
            data = int(char, base=10)
            yield (i, j, data)

def problem_data(filename):
    for line in _line_data(filename):
        yield line.removesuffix("\n")

def _line_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as problemfile:
        yield from problemfile
