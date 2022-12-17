import re
from dataclasses import dataclass
from typing import List, Set
from collections import defaultdict

RE_INT = re.compile(r"-?\d+")


def ints(s: str):
    return list(map(int, RE_INT.findall(s)))


def s():
    return [x.strip() for x in open("input.txt").readlines()]


from itertools import product

data = s()

names = [
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "zêta",
    "êta",
    "thêta",
    "iota",
    "kappa",
    "lambda",
    "mu",
    "nu",
    "xi",
    "omikron",
    "pi",
    "rho",
    "sigma",
    "tau",
    "upsilon",
    "phi",
    "chi",
    "psi",
    "omega"
]

next_mapping = 0
node_names = {}

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
    changed = False
    for i in range(len(data)):
        I = data[i]
        for j in range(len(data)):
            J = data[j]
            for k in range(len(data)):
                K = data[k]
                if distances[I.name, J.name] > distances[I.name, K.name] + distances[K.name, J.name]:
                    distances[I.name, J.name] = distances[I.name, K.name] + distances[K.name, J.name]
                    changed=True
    if not changed:
        break

print(distances)

data_cleaned = [p for p in data if p.flow_rate > 0 or p.name == "AA"]
import networkx as nx

G = nx.Graph()

node_colors = []
node_sizes = []

elephant_filter = {"RD", "JG", "EV", "HS", "WI", "EG", "ZV", "EG", "HO", "TJ"}
player_filter = {"FT", "WJ", "JH", "DV", "IQ", "KS", "RD", "JG", "HS"}

for p in data:
    G.add_node(p.name, size=p.flow_rate)
    node_colors.append("red" if p.flow_rate > 0 else "blue")
    node_sizes.append(50 if p.flow_rate > 0 else 20)

for p in data:
    G.add_weighted_edges_from([(p.name, c, distances[p.name, c]) for c in p.children])

import matplotlib.pyplot as plt

color_map = {p.name:"red" if p.flow_rate > 0 else "orange" for p in data}
color_map["AA"] = "green"

for i, a in enumerate(data):
    if a.name == "AA":
        node_colors[i] = "green"

#nx.draw(G, node_color=node_colors, with_labels=True, node_size=node_sizes)
#plt.show()


@dataclass()
class State:
    minutes: int
    position: str
    elephant_pos: str
    ttl: int
    elephant_ttl: int
    opened: Set[str]
    depth: int

    def get_greedy_value(self):
        player_options

    def get_options_from(self, pos):
        return [(p.name, distances[pos, p.name] + 1, p.flow_rate, p.flow_rate / (distances[pos, p.name] + 1)) for p in data if p.name not in self.opened]


def search(minutes, position, elephant_pos, ttl: int, elephant_ttl: int, opened: Set, depth=0):
    #print("\rSearching", position, "at minute", minutes, "opened are", opened)
    if ttl > 0 and elephant_ttl > 0:
        print("This never happens")
        return search(minutes-1, position, elephant_pos, ttl-1, elephant_ttl-1, opened)

    if depth <= 2:
        print("Starting iteration at depth", depth)

    options = [(p.name, distances[position, p.name]+1, p.flow_rate, p.flow_rate / (distances[position, p.name] + 1)) for p in data_cleaned if p.name not in opened]
    elephant_options = [(p.name, distances[elephant_pos, p.name]+1, p.flow_rate,p.flow_rate / (distances[elephant_pos, p.name] + 1)) for p in data_cleaned if p.name not in opened]
    options.sort(key=lambda o: o[1], reverse=False)
    elephant_options.sort(key=lambda o: o[1], reverse=False)
    options = options[:4]
    elephant_options = elephant_options[:4]

    if ttl == 0 and elephant_ttl == 0:
        value = 0
        best_option = None
        nodes = []
        i = 0
        for o, elephant_o in product(options, elephant_options):
            if o[0] == elephant_o[0]:
                continue
            elephant_shorter = distances[elephant_pos, o[0]] + 1 <= o[1]
            elephant_strictly_shorter = distances[elephant_pos, o[0]] + 1 < o[1]
            player_shorter = distances[position, elephant_o[0]] + 1 <= elephant_o[1]
            player_strictly_shorter = distances[position, elephant_o[0]] + 1 < elephant_o[1]
            if elephant_strictly_shorter and player_shorter:
                continue
            elif player_strictly_shorter and elephant_shorter:
                continue
            elif player_shorter and elephant_shorter and o[0] > elephant_o[0]:
                continue

            min_minutes = min(o[1], elephant_o[1])
            o_value = o[2] * (minutes - o[1]) + elephant_o[2] * (minutes - elephant_o[1])
            s_value, n = search(minutes - min_minutes, o[0], elephant_o[0], o[1]-min_minutes, elephant_o[1]-min_minutes, opened | {o[0], elephant_o[0]}, depth+1)
            if o_value + s_value > value:
                value = o_value + s_value
                best_option = o, elephant_o
                nodes = n
        return value, [best_option] + nodes

    if ttl == 0:
        value = 0
        best_option = None
        nodes = []
        for o in options:
            o_value = o[2] * (minutes - o[1])
            min_minutes = min(o[1], elephant_ttl)
            s_value, n = search(minutes - min_minutes, o[0], elephant_pos, o[1]-min_minutes, elephant_ttl-min_minutes, opened | {o[0]},depth+1)
            if o_value + s_value > value:
                value = o_value + s_value
                best_option = (o,)
                nodes = n
        return value, [best_option] + nodes

    if elephant_ttl == 0:
        value = 0
        best_option = None
        nodes = []
        for elephant_o in elephant_options:
            min_minutes = min(ttl, elephant_o[1])
            o_value = elephant_o[2] * (minutes - elephant_o[1])
            s_value, n = search(minutes - min_minutes, position, elephant_o[0], ttl-min_minutes, elephant_o[1]-min_minutes, opened | {elephant_o[0]},depth+1)
            if o_value + s_value > value:
                value = o_value + s_value
                best_option = (elephant_o,)
                nodes = n
        return value, [best_option] + nodes

from time import time

before_time = time()

value, nodes = search(26, "AA", "AA", 0, 0, set())

t = time() - before_time

print("Running time:", t, "seconds")

print(nodes)
print(value)

chosen = nodes
