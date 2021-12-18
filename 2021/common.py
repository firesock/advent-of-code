from __future__ import annotations

import os.path

from collections.abc import Iterator


class IntMap:
    rows: int
    cols: int
    array: list[list[int]]

    def __init__(self, array, cols, rows):
        self.array = array
        self.cols = cols
        self.rows = rows

    @staticmethod
    def filename(filename: str) -> IntMap:
        rows = []
        for i, line in enumerate(problem_data(filename)):
            col = []
            for j, char in enumerate(line):
                col.append(int(char, base=10))
            rows.append(col)

        return IntMap(rows, i + 1, j + 1)

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.array[key[0]][key[1]]

    def __iter__(self) -> Iterator[tuple[int, int, int]]:
        for i, row in enumerate(self.array):
            for j, data in enumerate(row):
                yield (i, j, data)


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
