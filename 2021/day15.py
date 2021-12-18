import collections
import heapq
import math

from typing import Literal, NewType, Union

from common import IntMap

Point = NewType('Point', tuple[int, int])

def neighbours(map_: IntMap) -> dict[Point, set[Point]]:
    neighbours = collections.defaultdict(set)
    for i in range(map_.cols):
        for j in range(map_.rows):
            for off_y, off_x in ((-1, 0), (0, 1), (0, -1), (1, 0)):
                potential = ((i + off_y, j + off_x))
                if -1 < potential[0] < map_.cols and -1 < potential[1] < map_.rows:
                    neighbours[(i, j)].add(potential)
    return neighbours


def cheapest_cost(risk_map: IntMap):
    class FrontierQueue:
        def __init__(self, initial: Point):
            entry = [0, initial]
            self.lookup = {initial: entry}
            self.heap = []
            heapq.heappush(self.heap, entry)

        def __delitem__(self, key: Point):
            entry = self.lookup.pop(key)
            entry[-1] = None

        def __setitem__(self, key: Point, value: int):
            try:
                del self[key]
            except KeyError:
                pass
            entry = [value, key]
            self.lookup[key] = entry
            heapq.heappush(self.heap, entry)

        def __len__(self):
            return len(self.lookup)

        def __contains__(self, key: Point):
            return key in self.lookup

        def __getitem__(self, key: Point):
            cost, point = self.lookup[key]
            return (cost, point)

        def pop(self):
            while True:
                cost, point = heapq.heappop(self.heap)
                if point is not None:
                    del self.lookup[point]
                    return (cost, point)

        def __iter__(self):
            return self

        def __next__(self):
            return self.pop()

    start = (0, 0)
    destination = (risk_map.rows - 1, risk_map.cols - 1)
    neighbours_ = neighbours(risk_map)
    distances = {(y, x): (math.inf, None)  for  y, x, _data in risk_map}
    distances[start] = (0, None)
    visited = set()
    frontier = FrontierQueue(start)

    while len(frontier) > 0:
        _cost, node = next(frontier)
        if node == destination:
            break
        visited.add(node)
        for neighbour in neighbours_[node]:
            cost = distances[node][0] + risk_map[neighbour]
            if neighbour not in visited and neighbour not in frontier:
                frontier[neighbour] = cost
                distances[neighbour] = (cost, node)
            elif neighbour in frontier:
                old_cost, point = frontier[neighbour]
                if cost < old_cost:
                    frontier[neighbour] = cost
                    distances[neighbour] = (cost, node)

    node = distances[destination]
    path = [destination, node[1]]
    while node[1] is not None:
        node = distances[node[1]]
        path.append(node[1])
    path.pop()
    path.reverse()

    # print(list(risk_map[p] for p in path))
    return distances[destination][0]

print(cheapest_cost(IntMap.filename("day15_sample.txt")))
print(cheapest_cost(IntMap.filename("day15_problem.txt")))

class RepeatedMap:
    def __init__(self, risk_map: IntMap, tiling: tuple[int, int]):
        y_multiple, x_multiple = tiling
        self.rows = risk_map.rows * y_multiple
        self.cols = risk_map.cols * x_multiple

        self.risk_map = risk_map

    def __getitem__(self, key: Point) -> int:
        y, x = key

        y_div, y_rem = divmod(y, self.risk_map.rows)
        x_div, x_rem = divmod(x, self.risk_map.cols)

        value = self.risk_map[(y_rem, x_rem)]
        return (((value - 1) + y_div + x_div) % 9) + 1


    def __iter__(self):
        for i in range(self.rows):
            for j in range(self.cols):
                yield (i, j, self[(i, j)])



print(cheapest_cost(RepeatedMap(IntMap.filename("day15_sample.txt"), (5, 5))))
print(cheapest_cost(RepeatedMap(IntMap.filename("day15_problem.txt"), (5, 5))))
