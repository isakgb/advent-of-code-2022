import re

RE_INT = re.compile(r"-?\d+")


def ints(s: str):
    return list(map(int, RE_INT.findall(s)))


def s():
    return [x.strip() for x in open("input.txt").readlines()]


data = s()

data = [ints(x) for x in data]

size = 4000000


def count_row(row):
    ranges = []
    for sx, sy, bx, by in data:
        taxicab = abs(sx - bx) + abs(sy - by)
        dist_at_row = taxicab - abs(row - sy)
        if dist_at_row > 0:
            ranges.append([sx-dist_at_row, sx+dist_at_row])

    s = set()

    interesting_positions = []

    for start, end in ranges:
        interesting_positions.extend([start - 1, start, end + 1])

    interesting_positions.sort()

    interesting_positions = [x for x in interesting_positions if 0 <= x <= size]

    for x in interesting_positions:
        for start, end in ranges:
            if start <= x <= end:
                break
        else:
            return x

    return None


for y in range(size):
    r = count_row(y)
    if r is not None:
        print(4000000*r+y)
        exit()
