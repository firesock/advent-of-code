from common import problem_data

sample_input = [int(s, base=10) for s in problem_data("day1_sample.txt")]
day1_input = [int(s, base=10) for s in problem_data("day1_problem.txt")]


def find_increases_count(input_list):
    increases = 0
    inputs = iter(input_list)
    last_input = next(inputs)
    for num in inputs:
        if num > last_input:
            increases += 1
        last_input = num
    return increases

print(find_increases_count(sample_input))
print(find_increases_count(day1_input))

def window3_gen(input_list):
    window = []
    for num in input_list:
        window.append(num)
        if len(window) == 3:
            yield sum(window)
            window.pop(0)

print(find_increases_count(window3_gen(sample_input)))
print(find_increases_count(window3_gen(day1_input)))
