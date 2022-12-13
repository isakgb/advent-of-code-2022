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


for i, pair in enumerate(data):
    cmp = check_order(pair)
    if cmp == 1:
        c += i + 1

print(c)
