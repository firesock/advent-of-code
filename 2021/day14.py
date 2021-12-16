import collections

from common import problem_data

def polymer_data(input_data):
    template = next(input_data)
    next(input_data) # newline

    pairs = {}
    for line in input_data:
        input_, output = line.split(" -> ")
        pairs[(input_[0], input_[1])] = output

    return (template, pairs)

def pair_insertion(template: str, pairs: dict[tuple[str, str], str]) -> str:
    new_template = []
    for p1, p2 in zip(template, template[1:]):
        new_template.append(p1)
        try:
            new_template.append(pairs[(p1, p2)])
        except KeyError:
            pass
    new_template.append(p2)
    return "".join(new_template)

def step_for(polymer_data, steps):
    template, pairs = polymer_data

    for _ in range(steps):
        template = pair_insertion(template, pairs)

    return template

print(len(step_for(polymer_data(problem_data("day14_sample.txt")), 5)))
print(len(step_for(polymer_data(problem_data("day14_sample.txt")), 10)))

def score_polymer(template):
    counter = collections.Counter(template)
    counts = counter.most_common()
    most = counts[0]
    least = counts[-1]

    return most[1] - least[1]


print(score_polymer(step_for(polymer_data(problem_data("day14_sample.txt")), 10)))
print(score_polymer(step_for(polymer_data(problem_data("day14_problem.txt")), 10)))

class Polymer:
    edges: collections.Counter
    start: tuple[str, str]

    def __init__(self, edges, start):
        self.edges = edges
        self.start = start

    @staticmethod
    def from_template(template: str):
        edges = collections.Counter()

        for p1, p2 in zip(template, template[1:]):
            edges[(p1, p2)] += 1

        return Polymer(edges, tuple(template[:2]))

    def __repr__(self):
        return f"{self.start} & {self.edges}"

def edges_insertion(polymer: Polymer, pairs: dict) -> Polymer:
    new_polymer = Polymer(collections.Counter(), polymer.start)
    for ((p1, p2), count) in polymer.edges.items():
        try:
            insertion = pairs[(p1, p2)]
            new_polymer.edges[(p1, insertion)] += count
            new_polymer.edges[(insertion, p2)] += count

            if (p1, p2) == polymer.start:
                new_polymer.start = (p1, insertion)
        except KeyError:
            new_polymer.edges[(p1, p2)] = count
    return new_polymer

def step_edges(polymer_data, steps):
    template, pairs = polymer_data
    polymer = Polymer.from_template(template)

    for _ in range(steps):
        polymer = edges_insertion(polymer, pairs)

    return polymer

def score_edges(polymer: Polymer):
    counter = collections.Counter()
    for ((p1, p2), count) in polymer.edges.items():
        counter[p2] += count

        if (p1, p2) == polymer.start:
            counter[p1] += count

    counts = counter.most_common()
    most = counts[0]
    least = counts[-1]
    return most[1] - least[1]

print(score_edges(step_edges(polymer_data(problem_data("day14_sample.txt")), 10)))
print(score_edges(step_edges(polymer_data(problem_data("day14_problem.txt")), 10)))

print(score_edges(step_edges(polymer_data(problem_data("day14_sample.txt")), 40)))
print(score_edges(step_edges(polymer_data(problem_data("day14_problem.txt")), 40)))
