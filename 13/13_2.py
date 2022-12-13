def s():
    return [x.strip() for x in open("input.txt").read().split("\n\n")]


data = s()

data = [d.split("\n") for d in data]

data = [[eval(c) for c in d] for d in data]


c = 0


def check_order(pair):
    left, right = pair
    for i in range(max(len(left), len(right))):
        if i == len(left) and i != len(right):
            return 1
        if i != len(left) and i == len(right):
            return 0

        l = left[i]
        r = right[i]

        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return 1
            elif r < l:
                return 0
            else:
                continue

        if isinstance(l, list) and isinstance(r, list):
            cmp = check_order([l, r])
            if cmp != -1:
                return cmp

        if isinstance(l, list) and isinstance(r, int):
            cmp = check_order([l, [r]])
            if cmp != -1:
                return cmp

        if isinstance(l, int) and isinstance(r, list):
            cmp = check_order([[l], r])
            if cmp != -1:
                return cmp

    return -1


def key(l, r):
    cmp = check_order([l, r])
    if cmp == 1:
        return -1
    if cmp == 0:
        return 1


all = []

for pair in data:
    all.extend(pair)
all.extend([[[2]],[[6]]])

for i in range(len(all)):
    for j in range(len(all)-1):
        if check_order([all[j], all[j+1]]) != 1:
            all[j], all[j+1] = all[j+1], all[j]


d1 = 0
d2 = 0

for i, d in enumerate(all):
    if d == [[2]]:
        d1 = i + 1
    elif d == [[6]]:
        d2 = i + 1

print(d1*d2)
