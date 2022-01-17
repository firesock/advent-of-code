
from __future__ import annotations

import itertools
import re

from typing import Iterable, Iterator

from common import problem_data


def deterministic(size: int) -> Iterator[int]:
    yield from itertools.cycle(range(1, size + 1))

def players(input_: Iterable[str]) -> list[tuple[int, int]]:
    players_ = []
    for line in input_:
        players_.append((int(re.sub(r"Player \d+ starting position: ", "", line), base=10), 0))
    return players_

sample_players = players(problem_data("day21_sample.txt"))
problem_players = players(problem_data("day21_problem.txt"))

def turn(player: tuple[int, int], dice: Iterator[int]) -> tuple[int, int]:
    pos, score = player
    pos -= 1
    for _i, roll in zip(range(3), dice):
        pos += roll
    pos = (pos % 10) + 1
    return (pos, score + pos)


class GameResult:
    @staticmethod
    def run(players_: Iterable[tuple[int, int]], win_score: int, dice: Iterator[int]) -> GameResult:
        result = GameResult()
        players_ = players_.copy()

        dice_rolls = 0
        def counting_rolls():
            nonlocal dice_rolls
            for roll in dice:
                dice_rolls += 1
                yield roll
        dice_ = counting_rolls()

        for i in itertools.cycle(range(len(players_))):
            pos, score = turn(players_[i], dice_)
            players_[i] = (pos, score)

            if score >= 1000:
                result.winner = (i, pos, score)
                break

        result.losers = [(j, player[0], player[1]) for j, player in enumerate(players_) if j != i]
        result.rolls = dice_rolls

        return result

    @property
    def two_player_loss_sum(self) -> int:
        assert len(self.losers) == 1
        return self.losers[0][2] * self.rolls


assert GameResult.run(sample_players, 1000, deterministic(100)).two_player_loss_sum == 739785
print(GameResult.run(problem_players, 1000, deterministic(100)).two_player_loss_sum)


def quantum_run(players_: Iterable[tuple[int, int]]) -> list[int]:
    rolls = list(sum(r) for r in itertools.product([1, 2, 3], repeat=3))
    wins = [0 for _p in players_]
    paired_score_buckets = {}
    for score_pair in itertools.product(range(21), repeat=len(wins)):
        paired_position_buckets = {}
        for pos_pair in itertools.product(range(1, 11), repeat=len(wins)):
            paired_position_buckets[tuple(pos_pair)] = 0
        paired_score_buckets[tuple(score_pair)] = paired_position_buckets
    poss = (p[0] for p in players_)
    scores = (p[1] for p in players_)
    paired_score_buckets[tuple(scores)][tuple(poss)] += 1

    for i in itertools.cycle(range(len(wins))):
        changes = []
        for score_pair, score_bucket in paired_score_buckets.items():
            for pos_pair, count in score_bucket.items():
                if count > 0:
                    changes.append((score_pair, pos_pair, -count))
                    for roll in rolls:
                        pos = ((pos_pair[i] - 1 + roll) % 10) + 1
                        score = score_pair[i] + pos
                        if score >= 21:
                            wins[i] += count
                        else:
                            new_pos_pair = pos_pair[:i] + (pos,) + pos_pair[i+1:]
                            new_score_pair = score_pair[:i] + (score,) + score_pair[i+1:]
                            changes.append((new_score_pair, new_pos_pair,  count))
        if len(changes) == 0:
            break
        for score_pair, pos_pair, change in changes:
            paired_score_buckets[score_pair][pos_pair] += change
    return wins

assert quantum_run(sample_players) == [444356092776315, 341960390180808]
print(quantum_run(problem_players))
