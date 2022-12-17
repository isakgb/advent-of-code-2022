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
blocked_coords = {(0,0), (1,0), (2,0), (3,0), (4,0),(5,0),(6,0)}


def shape_fits(rock, x, y):
    for dx, dy in rock:
        if ((x + dx), (y + dy)) in blocked_coords:
            return False
    return True


def get_blocked_coords(rock, x, y):
    b = set()
    for dx, dy in rock:
        b.add(((x + dx), (y + dy)))
    return b

height_increases = []
prev_highest_y = 0
rocks_fallen = 0


def simulate_rock():
    global next_rock, highest_y, next_jet, rocks_fallen
    rock = rocks[next_rock]
    width, height = wh[next_rock]
    next_rock = (next_rock + 1) % len(rocks)

    rock_x = 2
    rock_y = highest_y + 4
    rocks_fallen += 1

    while True:
        jet = data[next_jet]
        next_jet = (next_jet + 1) % len(data)
        if width <= rock_x + jet + width <= 7 and shape_fits(rock, rock_x + jet, rock_y):
            rock_x += jet
        if shape_fits(rock, rock_x, rock_y - 1):
            rock_y -= 1
        else:
            before_height = highest_y
            for dx,dy in rock:
                blocked_coords.add(((rock_x + dx), (rock_y + dy)))
                highest_y = (rock_y+dy) if rock_y+dy > highest_y else highest_y
            height_increase = highest_y - before_height
            height_increases.append(height_increase)
            break


for i in range(100000):
    simulate_rock()

pattern_length = 10
pattern = height_increases[-10:]
last_match = 0

for i in range(len(height_increases), 0, -1):
    if height_increases[i-10:i] == pattern:
        diff = last_match - i
        last_match = i

height_increase_per_cycle = sum(height_increases[-diff:])

cycle_length = diff


print("Cycle length", cycle_length, "height increases", height_increase_per_cycle)

remaining_rocks = 1000000000000 - rocks_fallen
num_cycles = remaining_rocks // cycle_length

remaining_rocks -= num_cycles * cycle_length

for i in range(remaining_rocks):
    simulate_rock()

highest_y += num_cycles * height_increase_per_cycle

print(highest_y)

