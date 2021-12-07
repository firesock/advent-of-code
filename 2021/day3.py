import itertools

from common import problem_data

def power_rates(binary_lines):
    first_line = next(binary_lines)
    b1_counts = [0 for b in first_line]
    for i, line in enumerate(itertools.chain([first_line], binary_lines)):
        for j, digit in enumerate(line):
            if digit == "1":
                b1_counts[j] += 1

    gamma_rate = 0
    epsilon_rate = 0
    half_total = i / 2
    for i, b1_count in enumerate(reversed(b1_counts)):
        if b1_count > half_total:
            gamma_rate += 1 << i
        else:
            epsilon_rate += 1 << i

    return (gamma_rate, epsilon_rate)

def csum(rates):
    r1, r2 = rates
    return r1 * r2

print(csum(power_rates(problem_data("day3_sample.txt"))))
print(csum(power_rates(problem_data("day3_problem.txt"))))

def life_support_rates(binary_lines):
    first_line = next(binary_lines)
    bitsize = len(first_line)
    numbers = [int(s, base=2) for s in itertools.chain([first_line], binary_lines)]

    def split_nums(nums, pos):
        mask = 1 << (bitsize - 1 - pos)
        one_in_pos = []
        zero_in_pos = []

        for num in nums:
            if (num & mask) == 0:
                zero_in_pos.append(num)
            else:
                one_in_pos.append(num)

        return (one_in_pos, zero_in_pos)

    def rating_search(nums, pos, comp):
        one_in_pos, zero_in_pos = split_nums(nums, pos)

        mask_pass = comp(one_in_pos, zero_in_pos)
        if len(mask_pass) == 1:
            return mask_pass[0]
        else:
            return rating_search(mask_pass, pos + 1, comp)

    def oxygen_comparison(one_in_pos, zero_in_pos):
        if len(zero_in_pos) > len(one_in_pos):
            return zero_in_pos
        else:
            return one_in_pos
    oxygen_rating = rating_search(numbers, 0, oxygen_comparison)

    def co2_comparison(one_in_pos, zero_in_pos):
        if len(one_in_pos) < len(zero_in_pos):
            return one_in_pos
        else:
            return zero_in_pos
    co2_rating = rating_search(numbers, 0, co2_comparison)

    return (oxygen_rating, co2_rating)

print(csum(life_support_rates(problem_data("day3_sample.txt"))))
print(csum(life_support_rates(problem_data("day3_problem.txt"))))
