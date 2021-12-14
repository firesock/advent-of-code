
import collections

from common import problem_data

def edges(input_data):
    connections = collections.defaultdict(set)
    for line in input_data:
        start, end = line.split("-")
        connections[start].add(end)
        connections[end].add(start)
    return connections

def complete_paths(edges):
    def walk_paths(current_path):
        last_node = current_path[-1]
        next_nodes = edges[last_node]
        new_paths = []
        for next_node in next_nodes:
            if next_node.upper() == "end".upper():
                new_paths.append(current_path + [next_node])
            elif next_node.isupper() or (next_node.islower() and next_node not in current_path):
                new_paths.extend(walk_paths(current_path + [next_node]))
        return new_paths

    return walk_paths(["start"])

print(len(complete_paths(edges(problem_data("day12_sample1.txt")))))
print(len(complete_paths(edges(problem_data("day12_sample2.txt")))))
print(len(complete_paths(edges(problem_data("day12_sample3.txt")))))
print(len(complete_paths(edges(problem_data("day12_problem.txt")))))

def complete_paths2(edges):
    def walk_paths(current_path, small_counter):
        last_node = current_path[-1]
        next_nodes = edges[last_node]
        new_paths = []
        for next_node in next_nodes:
            if next_node.upper() == "end".upper():
                new_paths.append(current_path + [next_node])
            elif next_node.upper() == "start".upper():
                pass
            elif next_node.isupper():
                new_paths.extend(walk_paths(current_path + [next_node], small_counter))
            else:
                if next_node not in current_path:
                    new_counter = small_counter.copy()
                    new_counter[next_node] += 1
                    new_paths.extend(walk_paths(current_path + [next_node], new_counter))
                else:
                    if not any(map(lambda v: v > 1, small_counter.values())):
                        new_counter = small_counter.copy()
                        new_counter[next_node] += 1
                        new_paths.extend(walk_paths(current_path + [next_node], new_counter))
        return new_paths

    return walk_paths(["start"], collections.Counter())

print(len(complete_paths2(edges(problem_data("day12_sample1.txt")))))
print(len(complete_paths2(edges(problem_data("day12_sample2.txt")))))
print(len(complete_paths2(edges(problem_data("day12_sample3.txt")))))
print(len(complete_paths2(edges(problem_data("day12_problem.txt")))))
