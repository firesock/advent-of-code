from common import problem_data

def fishes(input_data):
    line = next(input_data)
    return [int(f, base=10) for f in line.split(",")]

def tick_fishes(state):
    new_state = []
    for fish in state:
        ticked_fish = fish - 1
        if ticked_fish == -1:
            new_state.append(8)
            ticked_fish = 6
        new_state.append(ticked_fish)

    return new_state

def tick_days(state, days):
    for _ in range(days):
        state = tick_fishes(state)

    return state

print(len(tick_days(fishes(problem_data("day6_sample.txt")), 18)))
print(len(tick_days(fishes(problem_data("day6_sample.txt")), 80)))

print(len(tick_days(fishes(problem_data("day6_problem.txt")), 80)))

def bucket_fishes(input_data):
    line = next(input_data)
    buckets = [0 for _ in range(9)]

    for f in line.split(","):
        fish = int(f, base=10)
        buckets[fish] += 1

    return buckets

def tick_buckets(buckets):
    new_buckets = []
    spawning, ticking = buckets[0], buckets[1:]
    for bucket in ticking:
        new_buckets.append(bucket)
    new_buckets.append(0)

    new_buckets[6] += spawning
    new_buckets[8] += spawning

    return new_buckets

def tick_bucket_days(buckets, days):
    for _ in range(days):
        buckets = tick_buckets(buckets)

    return buckets

print(sum(tick_bucket_days(bucket_fishes(problem_data("day6_sample.txt")), 18)))
print(sum(tick_bucket_days(bucket_fishes(problem_data("day6_sample.txt")), 80)))

print(sum(tick_bucket_days(bucket_fishes(problem_data("day6_problem.txt")), 80)))

print(sum(tick_bucket_days(bucket_fishes(problem_data("day6_sample.txt")), 256)))
print(sum(tick_bucket_days(bucket_fishes(problem_data("day6_problem.txt")), 256)))

