from __future__ import annotations

import itertools
import functools
import math

from typing import Iterable, Iterator, Literal, Union

from common import problem_data

def output_trues(enhancement: str) -> list[int]:
    return list(map(lambda c: 1 if c == "#" else 0, enhancement))

class Image:
    @staticmethod
    def from_input_map(input_map: Iterable[Iterable[str]]) -> Image:
        image = Image()
        image.backing_value = 0
        image.first_point = (0, 0)
        image.lit_pixels = set()
        for i, row in enumerate(input_map):
            for j, c in enumerate(row):
                if c == "#":
                    image.lit_pixels.add((j, i))
        image.last_point = (j, i)
        return image

    @property
    def lit(self) -> Union[int, Literal[math.inf]]:
        if self.backing_value == 1:
            return math.inf
        else:
            return len(self.lit_pixels)

    def enhance(self, algo: list[int]) -> Image:
        image = Image()
        if self.backing_value == 0:
            image.backing_value = algo[0]
        else:
            image.backing_value = algo[511]
        image.first_point = (self.first_point[0] - 1, self.first_point[1] - 1)
        image.lit_pixels = set()
        for i in range(image.first_point[1], self.last_point[1] + 2):
            for j in range(image.first_point[0], self.last_point[0] + 2):
                lookup = 0
                for k, (i_d, j_d) in enumerate(reversed(list(itertools.product([-1, 0, 1], [-1, 0, 1])))):
                    p = (j + j_d, i + i_d)
                    if p in self.lit_pixels:
                        val = 1
                    elif p[0] < self.first_point[0] or p[0] > self.last_point[0] or p[1] < self.first_point[1] or p[1] > self.last_point[1]:
                        val = self.backing_value
                    else:
                        val = 0
                    lookup += val << k
                if algo[lookup] == 1:
                    image.lit_pixels.add((j, i))
        image.last_point = (j, i)
        return image

def parse(input_: Iterator[str]) -> tuple[list[int], Image]:
    algo = output_trues(next(input_))
    next(input_)  # ""
    image = Image.from_input_map(input_)
    return (algo, image)

sample_algo, sample_image = parse(problem_data("day20_sample.txt"))
problem_algo, problem_image = parse(problem_data("day20_problem.txt"))

def run(image: Image, algo: list[int], steps: 2) -> Image:
    return functools.reduce(Image.enhance, itertools.repeat(algo, steps), image)

assert run(sample_image, sample_algo, 2).lit == 35
print(run(problem_image, problem_algo, 2).lit)

assert run(sample_image, sample_algo, 50).lit == 3351
print(run(problem_image, problem_algo, 50).lit)
