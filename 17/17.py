def s():
    return [x.strip() for x in open("input.txt").read()]


wh = [
    [4, 1],
    [3, 3],
    [3, 3],
    [1, 4],
    [2, 2],
]

rocks = [[
    [0,0],
    [1,0],
    [2,0],
    [3,0],
],[
    [1,0],
    [0,1],
    [1,1],
    [2,1],
    [1,2],
],[
    [0,0],
    [1,0],
    [2,0],
    [2,1],
    [2,2],
],[
    [0,0],
    [0,1],
    [0,2],
    [0,3],
],
[
    [0,0],
    [0,1],
    [1,0],
    [1,1],
]
]

data = [-1 if x == "<" else 1 for x in s()]

next_rock = 0
highest_y = 0
next_jet = 0
blocked_coords = {(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)}


def shape_fits(rock, x, y):
    for dx, dy in rock:
        if ((x + dx), (y + dy)) in blocked_coords:
            return False
    return True


def cave_print(extra_blocked_coords=set()):
    for row in range(10, 0, -1):
        for col in range(7):
            c = "#" if (col, row) in blocked_coords else "."
            if (col, row) in extra_blocked_coords:
                c = "@"
            print(c, end="")
        print()


for i in range(2022):
    rock = rocks[next_rock]
    width, height = wh[next_rock]
    next_rock = (next_rock + 1) % len(rocks)

    rock_x = 2
    rock_y = highest_y + 4

    while True:
        jet = data[next_jet]
        next_jet = (next_jet + 1) % len(data)
        if width <= rock_x + jet + width <= 7 and shape_fits(rock, rock_x + jet, rock_y):
            rock_x += jet
        if shape_fits(rock, rock_x, rock_y - 1):
            rock_y -= 1
        else:
            for dx,dy in rock:
                blocked_coords.add(((rock_x + dx), (rock_y + dy)))
                highest_y = (rock_y+dy) if rock_y+dy > highest_y else highest_y
            break

cave_print()

print(highest_y)
