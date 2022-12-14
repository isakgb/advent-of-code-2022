from collections import defaultdict


def s():
    return [x.strip() for x in open("input.txt").readlines()]


data = s()


m = defaultdict(lambda: 0)

abyss_y = 0

for l in data:
    points = [[int(y) for y in x.split(",")] for x in l.split(" -> ")]

    for a,b in zip(points[:-1], points[1:]):
        x1, y1 = a
        x2, y2 = b

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                m[x1, y] = 2
                if y > abyss_y:
                    abyss_y = y
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)+1):
                m[x, y1] = 2
            if y1 > abyss_y:
                abyss_y = y1

abyss_y += 1

num_sand = 0

while True:
    sand_x = 500
    sand_y = 0

    if m[sand_x, sand_y] != 0:
        break

    while sand_y < abyss_y:
        if m[sand_x, sand_y + 1] == 0:
            sand_y += 1
            continue
        if m[sand_x - 1, sand_y + 1] == 0:
            sand_y += 1
            sand_x -= 1
            continue
        if m[sand_x + 1, sand_y + 1] == 0:
            sand_y += 1
            sand_x += 1
            continue
        m[sand_x, sand_y] = 1
        num_sand += 1
        break

    if sand_y == abyss_y:
        m[sand_x, sand_y] = 1
        num_sand += 1

print(num_sand)



