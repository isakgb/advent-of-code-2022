from collections import defaultdict
from heapq import heappop, heappush


def s():
    return [x.strip() for x in open("input.txt").readlines()]


data = s()

heights = defaultdict(lambda: None)

for y, line in enumerate(data):
    for x,  pixel in enumerate(line):
        if pixel == "S":
            start = x, y
        elif pixel == "E":
            end = x, y
        else:
            heights[x, y] = ord(pixel) - ord("a")


def adjacent(x, y, max_height):
    if (a := heights[x+1, y]) is not None and a >= max_height:
        yield a, (x+1, y)
    if (a := heights[x-1, y]) is not None and a >= max_height:
        yield a, (x-1, y)
    if (a := heights[x, y+1]) is not None and a >= max_height:
        yield a, (x, y+1)
    if (a := heights[x, y-1]) is not None and a >= max_height:
        yield a, (x, y-1)


visited = set()

heights[end] = 25
heights[start] = 0

h = []

heappush(h, (0, end))

while len(h) > 0:
    item = heappop(h)
    if item[1] in visited:
        continue

    visited.add(item[1])
    cost, [x, y] = item

    done = False

    height = heights[x, y]

    for adj in adjacent(x, y, height - 1):
        adj_cost, pos = adj
        if adj_cost == 0:
            print("Reached end in {} steps", cost+1)
            done = True
            break

        if adj not in visited:
            heappush(h, (cost + 1, pos))
    if done:
        break
