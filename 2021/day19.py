from __future__ import annotations

import collections
import functools
import itertools
import math
import operator

from typing import Iterable, Iterator, Mapping, NewType, Optional

from common import problem_data

def reports(lines: Iterator[str]) -> Iterator[list[tuple[int, int, int]]]:
    scanner_group = []
    for line in lines:
        if line.strip() == "":
            yield scanner_group
            scanner_group = []
        elif line.startswith("--- "):
            continue
        else:
            scanner_group.append(tuple(int(c, base=10) for c in line.split(",")))
    yield scanner_group

sample_reports = list(reports(problem_data("day19_sample.txt")))
problem_reports = list(reports(problem_data("day19_problem.txt")))

Transform = NewType("Transform", list[tuple[int, int, int]])

class BeaconRelations(dict):
    @classmethod
    def from_beacons(cls, beacons: Iterable[tuple[int, int, int]]) -> BeaconRelations:
        relations = cls()
        for beacon, relationships in itertools.groupby(itertools.permutations(beacons, 2), key=operator.itemgetter(0)):
            relations[beacon] = set()
            for (x1, y1, z1), (x2, y2, z2) in relationships:
                # relationship distances stay the same even as the axis pivots
                relations[beacon].add(frozenset((abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))))
        return relations

    def pairs(self, other: BeaconRelations, threshold: int=12) -> set[tuple[tuple[int, int, int], tuple[int, int, int]]]:
        paired = set()
        for (b1, r1), (b2, r2) in itertools.product(self.items(), other.items()):
            if (len(r1 & r2) + 1) >= threshold:  # +1 for examined beacon
                paired.add((b1, b2))
        return paired

    def reversal_transform(self, other: BeaconRelations) -> Optional[Transform]:
        pairs = self.pairs(other)
        reversal = None
        if len(pairs) > 0:
            # Just try all the possibilities until something is viable
            reversal = Transform([])
            for i, _self_axis in enumerate("xyz"):
                pair_iter = iter(pairs)
                self_p, other_p = next(pair_iter)

                possiblities = []
                for j, _other_axis in enumerate("xyz"):
                    for reflection in (-1, 1):
                        reflected_other_c = other_p[j] * reflection
                        diffs = [abs(abs(self_p[i]) - abs(reflected_other_c)), (abs(self_p[i]) + abs(reflected_other_c))]
                        for translation_f, diff in itertools.product((-1, 1), diffs):
                            possiblities.append((j, reflection, (translation_f * diff)))

                remaining_pairs = list(pair_iter)
                for possibility in possiblities:
                    j, reflection, diff = possibility
                    for self_p, other_p in remaining_pairs:
                        if ((other_p[j] * reflection) + diff) != self_p[i]:
                            break
                    else:
                        reversal.append(possibility)
                        break
            assert len(reversal) == 3
        return reversal

    def transform(self, transform_: Transform) -> BeaconRelations:
        relations = type(self)()
        x_t, y_t, z_t = transform_
        for beacon, relationships in self.items():
            x2 = (beacon[x_t[0]] * x_t[1]) + x_t[2]
            y2 = (beacon[y_t[0]] * y_t[1]) + y_t[2]
            z2 = (beacon[z_t[0]] * z_t[1]) + z_t[2]

            relations[(x2, y2, z2)] = relationships
        return relations

sample_beacon_relations = [BeaconRelations.from_beacons(s) for s in sample_reports]
problem_beacon_relations = [BeaconRelations.from_beacons(s) for s in problem_reports]

assert sample_beacon_relations[0].pairs(sample_beacon_relations[1]) == set([((-618, -824, -621), (686, 422, 578)), ((-537, -823, -458), (605, 423, 415)), ((-447, -329, 318), (515, 917, -361)), ((404, -588, -901), (-336, 658, 858)), ((544, -627, -890), (-476, 619, 847)), ((528, -643, 409), (-460, 603, -452)), ((-661, -816, -575), (729, 430, 532)), ((390, -675, -793), (-322, 571, 750)), ((423, -701, 434), (-355, 545, -477)), ((-345, -311, 381), (413, 935, -424)), ((459, -707, 401), (-391, 539, -444)), ((-485, -357, 347), (553, 889, -390))])

transform_10 = sample_beacon_relations[0].reversal_transform(sample_beacon_relations[1])
transform_41 = sample_beacon_relations[1].reversal_transform(sample_beacon_relations[4])
remapped_1_in_0 = sample_beacon_relations[1].transform(transform_10)
remapped_4_in_0 = sample_beacon_relations[4].transform(transform_41).transform(transform_10)

assert (remapped_1_in_0.keys() & remapped_4_in_0.keys()) == set([
    (459,-707,401),
    (-739,-1745,668),
    (-485,-357,347),
    (432,-2009,850),
    (528,-643,409),
    (423,-701,434),
    (-345,-311,381),
    (408,-1815,803),
    (534,-1912,768),
    (-687,-1600,576),
    (-447,-329,318),
    (-635,-1737,486),
])


def edges(nodes: Iterable[BeaconRelations]) -> dict[int, dict[int, Transform]]:
    edges_ = collections.defaultdict(dict)
    for (f, from_), (t, to) in itertools.permutations(enumerate(nodes), 2):
        reversal_transform = from_.reversal_transform(to)
        if reversal_transform is not None:
            edges_[t][f] = reversal_transform
    return dict(edges_)

sample_edges = edges(sample_beacon_relations)
problem_edges = edges(problem_beacon_relations)

def zero_paths(edges_: Mapping[int, Mapping[int, Transform]], nodes: Iterable[BeaconRelations]) -> dict[int, list[Transform]]:
    paths = [[n] for n in range(len(nodes))]

    finished_paths = []
    for i in itertools.count(2):
        if len(paths) == 0:
            break

        if i > len(nodes):
            raise Exception("Failed to path")

        new_paths = []
        for path in paths:
            for to, _transform in edges_[path[-1]].items():
                # shorter paths are possible, but requiring all in scanner 0 makes debugging easier
                if to == 0:
                    finished_paths.append(path + [to])
                elif to not in path:
                    new_paths.append(path + [to])
        paths = new_paths

    unity_paths_ = {n: [] for n in range(len(nodes))}
    for path in sorted(finished_paths, key=len):
        if unity_paths_[path[0]] == []:
            transform_path = []
            # itertools.pairwise follows
            p1, p2 = itertools.tee(path)
            next(p2, None)
            for from_, to in zip(p1, p2):
                transform_path.append(edges_[from_][to])
            unity_paths_[path[0]] = transform_path
    return unity_paths_

sample_zero_paths = zero_paths(sample_edges, sample_beacon_relations)
problem_zero_paths = zero_paths(problem_edges, problem_beacon_relations)

def zero_beacons(nodes: Iterable[BeaconRelations], paths: Mapping[int, list[Transform]]) -> BeaconRelations:
    transformed_nodes = []
    for i, node in enumerate(nodes):
        for transform in paths[i]:
            node = node.transform(transform)
        transformed_nodes.append(node)

    return functools.reduce(operator.or_, transformed_nodes)

sample_all_beacons_in_0 = zero_beacons(sample_beacon_relations, sample_zero_paths)
problem_all_beacons_in_0 = zero_beacons(problem_beacon_relations, problem_zero_paths)

assert sample_all_beacons_in_0.keys() == set([
    (-892,524,684),
    (-876,649,763),
    (-838,591,734),
    (-789,900,-551),
    (-739,-1745,668),
    (-706,-3180,-659),
    (-697,-3072,-689),
    (-689,845,-530),
    (-687,-1600,576),
    (-661,-816,-575),
    (-654,-3158,-753),
    (-635,-1737,486),
    (-631,-672,1502),
    (-624,-1620,1868),
    (-620,-3212,371),
    (-618,-824,-621),
    (-612,-1695,1788),
    (-601,-1648,-643),
    (-584,868,-557),
    (-537,-823,-458),
    (-532,-1715,1894),
    (-518,-1681,-600),
    (-499,-1607,-770),
    (-485,-357,347),
    (-470,-3283,303),
    (-456,-621,1527),
    (-447,-329,318),
    (-430,-3130,366),
    (-413,-627,1469),
    (-345,-311,381),
    (-36,-1284,1171),
    (-27,-1108,-65),
    (7,-33,-71),
    (12,-2351,-103),
    (26,-1119,1091),
    (346,-2985,342),
    (366,-3059,397),
    (377,-2827,367),
    (390,-675,-793),
    (396,-1931,-563),
    (404,-588,-901),
    (408,-1815,803),
    (423,-701,434),
    (432,-2009,850),
    (443,580,662),
    (455,729,728),
    (456,-540,1869),
    (459,-707,401),
    (465,-695,1988),
    (474,580,667),
    (496,-1584,1900),
    (497,-1838,-617),
    (527,-524,1933),
    (528,-643,409),
    (534,-1912,768),
    (544,-627,-890),
    (553,345,-567),
    (564,392,-477),
    (568,-2007,-577),
    (605,-1665,1952),
    (612,-1593,1893),
    (630,319,-379),
    (686,-3108,-505),
    (776,-3184,-501),
    (846,-3110,-434),
    (1135,-1161,1235),
    (1243,-1093,1063),
    (1660,-552,429),
    (1693,-557,386),
    (1735,-437,1738),
    (1749,-1800,1813),
    (1772,-405,1572),
    (1776,-675,371),
    (1779,-442,1789),
    (1780,-1548,337),
    (1786,-1538,337),
    (1847,-1591,415),
    (1889,-1729,1762),
    (1994,-1805,1792),
])
print(len(problem_all_beacons_in_0))

def zero_scanners(nodes: Iterable[BeaconRelations], paths: Mapping[int, list[Transform]]) -> list[tuple[int, int, int]]:
    return [next(iter(functools.reduce(BeaconRelations.transform, paths[i], BeaconRelations({(0, 0, 0): None})).keys())) for i in range(len(nodes))]


sample_scanners_in_zero = zero_scanners(sample_beacon_relations, sample_zero_paths)
problem_scanners_in_zero = zero_scanners(problem_beacon_relations, problem_zero_paths)

assert sample_scanners_in_zero == [(0, 0, 0), (68, -1246, -43), (1105, -1205, 1229), (-92, -2380, -20), (-20, -1133, 1061)]

def largest_manhattan(scanners: Iterable[tuple[int, int, int]]) -> int:
    largest = -math.inf
    for s1, s2 in itertools.combinations(scanners, 2):
        dist = abs(s1[0] - s2[0]) + abs(s1[1] - s2[1]) + abs(s1[2] - s2[2])
        largest = max(largest, dist)
    return largest

sample_largest_distance = largest_manhattan(sample_scanners_in_zero)
problem_largest_distance = largest_manhattan(problem_scanners_in_zero)

assert sample_largest_distance == 3621
print(problem_largest_distance)
