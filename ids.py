from typing import List
import numpy as np
import re
from copy import deepcopy
from itertools import permutations


def produce_start_node(start_queue):
    pattern = re.compile("([0-9]+)([a-zA-Z]+)")
    start_q = []
    square = None
    for r in range(shape[0]):
        row = []
        for c in range(shape[1]):
            if start_queues[r][c] == '#':
                square = (r, c)
            else:
                row.append(pattern.match(start_queue[r][c]).groups())
        start_q.append(row)
    start_q[square[0]].insert(square[1], '#')
    return Node(start_q, square, 0)


class Node:
    def __init__(self, queues, sq, d):
        self.next_nodes = []
        self.queues = queues
        self.square = sq
        self.depth = d
        self.parent: Node = None

    # a method that produces nodes neighbours
    def produce_children(self):
        if self.next_nodes:
            return
        direction = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        sh = np.shape(self.queues)
        for d in direction:
            x = self.square[0] + d[0]
            y = self.square[1] + d[1]
            if x < 0 or y < 0 or x >= sh[0] or y >= sh[1]:
                continue
            q = deepcopy(self.queues)
            q[self.square[0]][self.square[1]] = q[x][y]
            q[x][y] = '#'
            s = (x, y)
            child = Node(q, s, self.depth + 1)
            child.parent = self
            self.next_nodes.append(child)


class Graph:

    def __init__(self, minimum, maximum, st: Node):
        self.first_depth = minimum
        self.frontier: List[Node] = []
        self.max_limit = maximum
        self.goals = []
        self.start = st
        self.path = []
        self.produce_goals()
        self.nodes_produced = 0
        self.nodes_explored = 0

    def is_goal(self, node):
        for g in self.goals:
            if g == node.queues:
                return True
        return False

    def recursive_dls(self, depth, node: Node):
        if self.is_goal(node):
            self.path.append(node)
            return True
        if depth <= 0:
            return False
        self.nodes_explored += 1
        node.produce_children()
        for n in node.next_nodes:
            self.nodes_produced += 1
            if self.recursive_dls(depth - 1, n):
                self.path.insert(0, node)
                return True
        return False

    # the main method that increases the depth of dls search to maximum limit that user has set
    def ids(self):
        for lim in range(self.first_depth,self.max_limit):
            print('\n\n', lim)
            self.frontier = []
            res = self.recursive_dls(lim, self.start)
            if res:
                print('found')
                break
            else:
                print('nodes explored so far', self.nodes_explored)
                print('nodes produced so far', self.nodes_produced)
        else:
            print('sorry not found')

    # it produces a set of goal possibilities to compare nodes to
    def produce_goals(self):
        letters = {}
        for ro in range(shape[0]):
            for co in range(shape[1]):
                if self.start.queues[ro][co] == '#':
                    continue
                if self.start.queues[ro][co][1] in letters.keys():
                    letters[self.start.queues[ro][co][1]].append(self.start.queues[ro][co])
                else:
                    letters[self.start.queues[ro][co][1]] = [self.start.queues[ro][co]]
        goal_queues = []
        for key in letters.keys():
            if len(letters[key]) < shape[1]:
                limit = sorted(letters[key], reverse=True)
                limit.insert(0, '#')
                goal_queues.append(limit)
            else:
                goal_queues.append(sorted(letters[key], reverse=True))
        for p in permutations(goal_queues):
            self.goals.append(list(p))

    def print_path(self):
        for i in self.path:
            for line in i.queues:
                print(line)
            print('\n\n')


# getting input from user
shape = list(map(int, input().split()))
start_queues = []
for i in range(shape[0]):
    start_queues.append(list(input().split()))
start = produce_start_node(start_queues)
my_graph = Graph(minimum=3, maximum=20, st=start)
my_graph.ids()
my_graph.print_path()

print('nodes explored', my_graph.nodes_explored)
print('nodes produced', my_graph.nodes_produced)
