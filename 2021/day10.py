from __future__ import annotations

import enum

from typing import Optional

from common import problem_data

class Parse:
    class Result(enum.Enum):
        OK = enum.auto()
        CORRUPT = enum.auto()
        INCOMPLETE = enum.auto()

    result: Parse.Result

    def __init__(self, result: Parse.Result):
        self.result = result

    @staticmethod
    def ok(completed: str) -> Parse:
        p = Parse(Parse.Result.OK)
        p.completed = complete
        return p

    @staticmethod
    def corrupt(expected: str, found: str) -> Parse:
        p = Parse(Parse.Result.CORRUPT)
        p.expected = expected
        p.found = found
        return p

    @staticmethod
    def incomplete(expected: str, read: str) -> Parse:
        p = Parse(Parse.Result.INCOMPLETE)
        p.expected = expected
        p.read = read
        return p

PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
OPENERS = frozenset(PAIRS.keys())
CLOSERS = frozenset(PAIRS.values())


def parse_line(line: str) -> Parse:
    expected = [PAIRS[line[0]]]
    for char in line[1:]:
        if char in CLOSERS:
            expected_char = expected.pop()
            if expected_char != char:
                return Parse.corrupt(expected_char, char)

        if char in OPENERS:
            expected.append(PAIRS[char])

    if len(expected) == 0:
        return Parse.ok(line)
    else:
        return Parse.incomplete("".join(reversed(expected)), line)

ILLEGALS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

def score_illegals(data):
    score = 0
    for line in data:
        parse = parse_line(line)
        if parse.result is Parse.Result.CORRUPT:
            score += ILLEGALS[parse.found]
    return score

print(score_illegals(problem_data("day10_sample.txt")))
print(score_illegals(problem_data("day10_problem.txt")))

INCOMPLETES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

def score_incompletes(data):
    scores = []
    for line in data:
        parse = parse_line(line)
        if parse.result is Parse.Result.INCOMPLETE:
            score = 0
            for char in parse.expected:
                score = ((5 * score) + INCOMPLETES[char])
            scores.append(score)
    return scores

def middle(scores):
    return sorted(scores)[len(scores) // 2]

print(middle(score_incompletes(problem_data("day10_sample.txt"))))
print(middle(score_incompletes(problem_data("day10_problem.txt"))))
