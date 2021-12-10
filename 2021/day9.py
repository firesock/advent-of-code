import itertools

from typing import NamedTuple, Iterable, NewType

from common import problem_data

def point_adjacents(input_data):
    heightmap = list(input_data)

    for i, line in enumerate(heightmap):
        for j, value in enumerate(line):
            height = int(value, base=10)
            adjacents = []
            if i > 0:
                adjacents.append(heightmap[i - 1][j])
            if i < len(heightmap) - 1:
                adjacents.append(heightmap[i + 1][j])
            if j > 0:
                adjacents.append(heightmap[i][j - 1])
            if j < len(line) - 1:
                adjacents.append(heightmap[i][j + 1])

            yield (height, frozenset(int(a, base=10) for a in adjacents))


def low_points(point_stars):
    for point, adjacents in point_stars:
        for adjacent in adjacents:
            if adjacent <= point:
                break
        else:
            yield point

def sum_low_points(point_stars):
    count = 0
    for low_point in low_points(point_stars):
        count += low_point + 1
    return count

print(sum_low_points(point_adjacents(problem_data("day9_sample.txt"))))
print(sum_low_points(point_adjacents(problem_data("day9_problem.txt"))))

Point = NewType('Point', tuple[int, int])

class HeightMap:
    array: list[list[int]]
    rows: int
    cols: int
    ridges: frozenset[Point]

    def __init__(self, input_data: Iterable[str]):
        heightmap = list(input_data)

        self.array = []
        ridges = []
        for i, line in enumerate(heightmap):
            line_array = []
            for j, value in enumerate(line):
                height = int(value, base=10)
                line_array.append(height)
                if height == 9:
                    ridges.append((i, j))
            self.array.append(line_array)

        self.ridges = frozenset(ridges)
        self.rows = i + 1
        self.cols = j + 1

def grow_point(point_coords: Point, hmap: HeightMap) -> frozenset[Point]:
    y, x = point_coords

    potential_growth = set()
    if y > 0:
        potential_growth.add((y - 1, x))
    if y < hmap.rows - 1:
        potential_growth.add((y + 1, x))
    if x > 0:
        potential_growth.add((y, x - 1))
    if x < hmap.cols - 1:
        potential_growth.add((y, x + 1))

    return frozenset(p for p in potential_growth if p not in hmap.ridges)

Basin = NewType('Basin', frozenset[Point])

def basins(input_data: Iterable[str]) -> list[Basin]:
    hmap = HeightMap(input_data)
    all_points = set(p for p in itertools.product(range(hmap.rows), range(hmap.cols)) if p not in hmap.ridges)
    basins = []

    while len(all_points) > 0:
        basin = set()
        growing_points = set([all_points.pop()])
        while len(growing_points) > 0:
            current_point = growing_points.pop()
            new_points = grow_point(current_point, hmap)
            growing_points.update(new_points - basin)
            basin.add(current_point)
        basins.append(frozenset(basin))
        all_points.difference_update(basin)

    return basins

def basins_3sum(basins: list[Basin]) -> int:
    count = 1
    for basin in sorted(basins, key=len, reverse=True)[:3]:
        count *= len(basin)
    return count

print(basins_3sum(basins(problem_data("day9_sample.txt"))))
print(basins_3sum(basins(problem_data("day9_problem.txt"))))
