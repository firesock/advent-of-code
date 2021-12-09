import collections

from common import problem_data
from typing import Iterable

segment_count_map = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}

def count_uniques(input_data):
    unique_counts = frozenset(v for k, v in segment_count_map.items() if k in (1, 4, 7, 8))

    count = 0
    for line in input_data:
        _segments, outputs = line.split(" | ")
        output_segments = outputs.split(" ")
        for output_segment in output_segments:
            if len(output_segment) in unique_counts:
                count += 1

    return count

print(count_uniques(problem_data("day8_sample.txt")))
print(count_uniques(problem_data("day8_problem.txt")))


def mappings(unique_patterns: Iterable[frozenset]) -> dict[frozenset, int]:
    len_to_patterns = collections.defaultdict(list)
    for pattern in unique_patterns:
        len_to_patterns[len(pattern)].append(pattern)

    digit_to_pattern = {
        1: len_to_patterns[2][0],
        4: len_to_patterns[4][0],
        7: len_to_patterns[3][0],
        8: len_to_patterns[7][0],
    }

    for pattern in len_to_patterns[6]:
        if not digit_to_pattern[1].issubset(pattern):
            digit_to_pattern[6] = pattern
        else:
            if digit_to_pattern[4].issubset(pattern):
                digit_to_pattern[9] = pattern
            else:
                digit_to_pattern[0] = pattern

    for pattern in len_to_patterns[5]:
        if not digit_to_pattern[1].issubset(pattern):
            if pattern.issubset(digit_to_pattern[6]):
                digit_to_pattern[5] = pattern
            else:
                digit_to_pattern[2] = pattern
        else:
            digit_to_pattern[3] = pattern

    return {v: k for k, v in digit_to_pattern.items()}

def output(line):
    patterns, output_patterns = line.split(" | ")
    pattern_to_digit = mappings(frozenset(p) for p in patterns.split())

    output = 0
    for i, pattern in enumerate(reversed(output_patterns.split())):
        output += pattern_to_digit[frozenset(pattern)] * (10 ** i)

    return output

print(output("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"))

def totals(input_data):
    return sum(output(line) for line in input_data)

print(totals(problem_data("day8_sample.txt")))
print(totals(problem_data("day8_problem.txt")))
