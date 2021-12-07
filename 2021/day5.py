import collections

from common import problem_data

def endpoints(line_data):
    def c(s):
        return int(s, base=10)

    for line in line_data:
        start, end = line.split(" -> ")
        x1, y1 = start.split(",")
        x2, y2 = end.split(",")

        yield ((c(x1), c(y1)), (c(x2), c(y2)))


def straight_line_points(lines):
    for endpoints in lines:
        ((x1, y1), (x2, y2)) = endpoints
        if x1 == x2:
            start = min(y1, y2)
            end = max(y1, y2)
            for y in range(start, end + 1):
                yield (x1, y)
        elif y1 == y2:
            start = min(x1, x2)
            end = max(x1, x2)
            for x in range(start, end + 1):
                yield (x, y1)


def find_2overlap(points):
    counter = collections.Counter()

    for point in points:
        counter[point] += 1

    overlaps = 0
    for _point, count in counter.most_common():
        if count < 2:
            break
        elif count >= 2:
            overlaps += 1

    return overlaps


print(find_2overlap(straight_line_points(endpoints(problem_data("day5_sample.txt")))))
print(find_2overlap(straight_line_points(endpoints(problem_data("day5_problem.txt")))))

def line_points(lines):
    for endpoints in lines:
        ((x1, y1), (x2, y2)) = endpoints
        if x1 == x2:
            xstep = 0
        elif x1 < x2:
            xstep = 1
        else:
            xstep = -1
        if y1 == y2:
            ystep = 0
        elif y1 < y2:
            ystep = 1
        else:
            ystep = -1

        coord = (x1, y1)
        while coord != (x2, y2):
            yield coord
            x, y = coord
            coord = (x+xstep, y+ystep)
        yield coord

print(find_2overlap(line_points(endpoints(problem_data("day5_sample.txt")))))
print(find_2overlap(line_points(endpoints(problem_data("day5_problem.txt")))))
