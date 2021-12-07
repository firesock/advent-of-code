import os.path

def problem_data(filename):
    for line in _line_data(filename):
        yield line.removesuffix("\n")

def _line_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as problemfile:
        yield from problemfile
