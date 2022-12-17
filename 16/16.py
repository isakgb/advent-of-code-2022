import re
from dataclasses import dataclass
from typing import List, Set
from collections import defaultdict


RE_INT = re.compile(r"-?\d+")


def ints(s: str):
    return list(map(int, RE_INT.findall(s)))


def s():
    return [x.strip() for x in open("input.txt").readlines()]


data = s()


@dataclass()
class Pipe:
    name: str
    flow_rate: int
    children: List[str]

    @staticmethod
    def from_line(line):
        l = line.split(" ")
        name = l[1]
        flow_rate = ints(line)[0]
        children = l[9:]
        children = [c[:2] for c in children]
        return Pipe(name, flow_rate, children)


data = [Pipe.from_line(x) for x in data]
pipe = {pipe.name: pipe for pipe in data}

distances = defaultdict(lambda: 1000)

for pipe in data:
    distances[pipe.name, pipe.name] = 0
    for child in pipe.children:
        distances[pipe.name, child] = 1

for f in range(len(data)):
    for i in range(len(data)):
        I = data[i]
        for j in range(len(data)):
            J = data[j]
            for k in range(len(data)):
                K = data[k]
                if distances[I.name, J.name] > distances[I.name, K.name] + distances[K.name, J.name]:
                    distances[I.name, J.name] = distances[I.name, K.name] + distances[K.name, J.name]

print(distances)

def search(minutes, position, opened: Set):
    #print("\rSearching", position, "at minute", minutes, "opened are", opened)
    options = [(p.name, distances[position, p.name]+1, p.flow_rate) for p in data if p.flow_rate > 0 and p.name not in opened]
    if len(options) == 0:
        return 0, []
    value = 0
    best_option = None
    nodes = []
    for o in options:
        if minutes - o[1] <= 0:
            continue
        s_value, n = search(minutes - o[1], o[0], opened | {o[0]})
        o_value = o[2] * (minutes - o[1]) + s_value
        if o_value > value:
            value = o_value
            best_option = o[0]
            nodes = n
    #print("Value was", value)
    return value, [best_option] + nodes


value, nodes = search(30, "AA", set())
print(value)

chosen = nodes
print(nodes)
total_released = 0
minutes = 30
pos = "ZN"
for c in chosen:
    if c is None:
        continue
    print("Distance", pos, "->", c, " = ", distances[pos, c])
    minutes -= distances[pos, c] + 1
    pipe = next(p for p in data if p.name == c)
    print("Opening valve", pipe.name, "at minute", minutes, "releasing a total of", pipe.flow_rate * minutes)
    total_released += pipe.flow_rate * minutes
    pos = c

print(total_released)


a, b = search(6, "JH", {'HS', 'WI', 'EV', 'RD', 'WJ', 'DV', 'JH'})


"1584 is too high"

print(a,b)


