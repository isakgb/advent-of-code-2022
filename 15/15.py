import re

RE_INT = re.compile(r"-?\d+")


def ints(s: str):
    return list(map(int, RE_INT.findall(s)))


def s():
    return [x.strip() for x in open("input.txt").readlines()]


data = s()

data = [ints(x) for x in data]

ranges = []

banned_x = set()


def count_row(row):
    for sx, sy, bx, by in data:
        taxicab = abs(sx - bx) + abs(sy - by)
        dist_at_row = taxicab - abs(row - sy)
        if dist_at_row > 0:
            print(sx, sy, bx, by)
            ranges.append([sx-dist_at_row, sx+dist_at_row])
        if by == row:
            banned_x.add(bx)

    s = set()

    for start, end in ranges:
        for i in range(start, end + 1):
            s.add(i)

    s -= banned_x

    return len(s)


print(count_row(2000000))
