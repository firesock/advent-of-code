import ast
import itertools
import math

from typing import Iterable, NewType, Optional, Union

from common import problem_data

UnreducedSNum = NewType("UnreducedSNum", list[str])
SNum = NewType("SNum", list[str])
LiteralSNum = NewType("LiteralSNum", Union[list, int])  # Badly-typed recursive

def snum_create(text: str) -> UnreducedSNum:
    snum = []
    for c in text:
        if c in "[],":
            snum.append(c)
        else:
            snum.append(int(c, base=10))
    return snum

def snum_reduce_step(snum: UnreducedSNum) -> Optional[UnreducedSNum]:
    new_snum = []
    depth = 0
    last_left = None
    snum_iter = enumerate(snum)
    while (elem := next(snum_iter, None)) is not None:
        i, e = elem
        assert depth < 6  # SNum's with this depth haven't been reduced correctly
        if e == "[":
            depth += 1
        elif e == "]":
            depth -= 1
        elif isinstance(e, int):
            if depth == 5:
                left = e
                next(snum_iter)  # ","
                right = next(snum_iter)[1]
                next(snum_iter)  # "]"

                new_snum.pop(-1)  # "["
                if last_left is not None:
                    new_snum[last_left] += left
                new_snum.append(0)
                for _i, e in snum_iter:
                    if isinstance(e, int):
                        new_snum.append(e + right)
                        break
                    new_snum.append(e)
                new_snum.extend(e for _i, e in snum_iter)
                break
            last_left = i
        new_snum.append(e)
    else:
        snum = new_snum
        new_snum = []
        snum_iter = iter(snum)
        while (e := next(snum_iter, None)) is not None:
            if isinstance(e, int) and e > 9:
                left = math.floor(e / 2)
                right = math.ceil(e / 2)
                new_snum.extend(["[", left, ",", right, "]"])
                new_snum.extend(snum_iter)
                break
            new_snum.append(e)
        else:
            return None
    return new_snum

def snum_reduce(snum: UnreducedSNum) -> SNum:
    while (new_snum := snum_reduce_step(snum)) is not None:
        snum = new_snum
    return snum

def snum(text: str) -> SNum:
    return snum_reduce(snum_create(text))

def text(snum: Union[UnreducedSNum, SNum]) -> str:
    text_snum = []
    for c in snum:
        if isinstance(c, int):
            text_snum.append(str(c))
        else:
            text_snum.append(c)
    return "".join(text_snum)

assert text(snum("[[[[[9,8],1],2],3],4]")) == "[[[[0,9],2],3],4]"
assert text(snum("[7,[6,[5,[4,[3,2]]]]]")) == "[7,[6,[5,[7,0]]]]"
assert text(snum("[[6,[5,[4,[3,2]]]],1]")) == "[[6,[5,[7,0]]],3]"
# Single explode action example is not copied
assert text(snum("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
assert text(snum("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

def add(a: SNum, b: SNum) -> SNum:
    return snum_reduce(["[", *a, ",", *b, "]"])

assert text(add(snum("[[[[4,3],4],4],[7,[[8,4],9]]]"), snum("[1,1]"))) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

def sum_list(snum_texts: Iterable[str]) -> SNum:
    total = snum(next(snum_texts))
    for snum_text in snum_texts:
        total = add(total, snum(snum_text))
    return total

assert text(sum_list(problem_data("day18_sample1.txt"))) == "[[[[1,1],[2,2]],[3,3]],[4,4]]"
assert text(sum_list(problem_data("day18_sample2.txt"))) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"
assert text(sum_list(problem_data("day18_sample3.txt"))) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"
assert text(sum_list(problem_data("day18_sample4.txt"))) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
assert text(sum_list(problem_data("day18_sample5.txt"))) == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"


def literal(snum: SNum) -> LiteralSNum:
    return ast.literal_eval(text(snum))

def magnitude(snum: LiteralSNum) -> int:
    if isinstance(snum, int):
        return snum
    else:
        return (magnitude(snum[0]) * 3) + (magnitude(snum[1]) * 2)

assert magnitude(literal(snum("[[9,1],[1,9]]"))) == 129
assert magnitude(literal(snum("[[1,2],[[3,4],5]]"))) == 143
assert magnitude(literal(snum("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"))) == 1384
assert magnitude(literal(snum("[[[[1,1],[2,2]],[3,3]],[4,4]]"))) == 445
assert magnitude(literal(snum("[[[[3,0],[5,3]],[4,4]],[5,5]]"))) == 791
assert magnitude(literal(snum("[[[[5,0],[7,4]],[5,5]],[6,6]]"))) == 1137
assert magnitude(literal(snum("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"))) == 3488

assert magnitude(literal(sum_list(problem_data("day18_sample5.txt")))) == 4140
print(magnitude(literal(sum_list(problem_data("day18_problem.txt")))))

def largest_sum(snums: list[SNum]) -> int:
    largest = -math.inf
    for snum1, snum2 in itertools.permutations(snums, 2):
        snum_add = add(snum1, snum2)
        mag = magnitude(literal(snum_add))
        largest = max(largest, mag)
    return largest

assert largest_sum(list(snum(s) for s in problem_data("day18_sample5.txt"))) == 3993
print(largest_sum(list(snum(s) for s in problem_data("day18_problem.txt"))))
