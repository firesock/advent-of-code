import itertools

from common import problem_data

def area(input_data: str) -> tuple[tuple[int, int], tuple[int, int]]:
    x_part, y_part = input_data.split(", ")
    x_start, x_end = x_part.removeprefix("target area: x=").split("..")
    y_start, y_end = y_part.removeprefix("y=").split("..")

    return (
        (int(x_start, base=10), int(x_end, base=10)),
        (int(y_start, base=10), int(y_end, base=10)),
    )

sample_area = area(next(problem_data("day17_sample.txt")))
problem_area = area(next(problem_data("day17_problem.txt")))

def x_possibilities(area_):
    (x_start, x_end), _ = area_
    destination_range = frozenset(range(x_start, x_end + 1))
    state_trackers = [(v, v, 0) for v in range(0, x_end + 1)]
    possibilities = []
    for steps in itertools.count(1):
        next_trackers = []
        for initial_velocity, velocity, position in state_trackers:
            new_velocity = velocity - 1
            new_position = position + velocity

            if x_start <= new_position <= x_end:
                possibilities.append(initial_velocity)
            elif new_velocity > 0:
                next_trackers.append((initial_velocity, new_velocity, new_position))
        state_trackers = next_trackers
        if len(state_trackers) == 0:
            break
    return possibilities

sample_x_pos = x_possibilities(sample_area)
problem_x_pos = x_possibilities(problem_area)

def y_possibilities(area_):
    _, (y_start, y_end) = area_
    possibilities = []
    successes = set()
    failures = set()
    for initial_velocity in itertools.count(y_start):
        steps = [(0, initial_velocity)]
        success = False
        while True:
            position, velocity = steps[-1]
            if steps[-1] in successes or y_start <= position <= y_end:
                success = True
                break
            elif steps[-1] in failures or position < y_start:
                break
            steps.append((position + velocity, velocity - 1))

        if success is True:
            possibilities.append(initial_velocity)
            successes.update(steps)
        else:
            failures.update(steps)
            # Going from 0 with a velocity greater than y_start won't change at
            # higher velocities, it will just be faster to overshoot
            if steps[-2][0] == 0 and steps[-1][1] < y_start:
                break
    return possibilities

sample_y_pos = y_possibilities(sample_area)
problem_y_pos = y_possibilities(problem_area)

def max_y(area_, x_velocities, y_velocities):
    (x_start, x_end), (y_start, y_end) = area_
    total_max_y = 0
    state_trackers = [(0, (0, 0), (x_v, y_v)) for x_v, y_v in itertools.product(x_velocities, y_velocities)]

    for _step in itertools.count(0):
        next_trackers = []
        for max_y, (x_p, y_p), (x_v, y_v) in state_trackers:
            x2_p = x_p + x_v
            y2_p = y_p + y_v
            max_y2 = max(max_y, y2_p)
            if x_start <= x2_p <= x_end and y_start <= y2_p <= y_end:
                total_max_y = max(total_max_y, max_y2)
            elif x2_p <= x_end and y2_p > y_start:
                if x_v > 0:
                    x2_v = x_v - 1
                elif x_v < 0:
                    x2_v = x_v + 1
                else:
                    x2_v = x_v
                y2_v = y_v - 1
                next_trackers.append((max_y2, (x2_p, y2_p), (x2_v, y2_v)))
        state_trackers = next_trackers
        if len(state_trackers) == 0:
            break

    return total_max_y

print(max_y(sample_area, sample_x_pos, sample_y_pos))
print(max_y(problem_area, problem_x_pos, problem_y_pos))

def successes(area_, x_velocities, y_velocities):
    (x_start, x_end), (y_start, y_end) = area_
    state_trackers = [((x_v, y_v), (0, 0), (x_v, y_v)) for x_v, y_v in itertools.product(x_velocities, y_velocities)]
    reached = []

    for _step in itertools.count(0):
        next_trackers = []
        for initial_velocities, (x_p, y_p), (x_v, y_v) in state_trackers:
            x2_p = x_p + x_v
            y2_p = y_p + y_v
            if x_start <= x2_p <= x_end and y_start <= y2_p <= y_end:
                reached.append(initial_velocities)
            elif x2_p <= x_end and y2_p > y_start:
                if x_v > 0:
                    x2_v = x_v - 1
                elif x_v < 0:
                    x2_v = x_v + 1
                else:
                    x2_v = x_v
                y2_v = y_v - 1
                next_trackers.append((initial_velocities, (x2_p, y2_p), (x2_v, y2_v)))
        state_trackers = next_trackers
        if len(state_trackers) == 0:
            break

    return reached

print(len(successes(sample_area, sample_x_pos, sample_y_pos)))
print(len(successes(problem_area, problem_x_pos, problem_y_pos)))
