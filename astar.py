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
    def __init__(self, queues, sq, g):
        self.next_nodes = []
        self.queues = queues
        self.square = sq
        self.g = g
        self.h = 0
        self.parent: Node = None

    def produce_children(self):
        direction = [(-1, 0), (1, 0), (0, 1), (0, -1)]
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
            ch = Node(q, s, self.g + 1)
            ch.parent = self
            self.next_nodes.append(ch)
        return self.next_nodes


class Graph:

    def __init__(self, start_node: Node, ro, co):
        self.explored = []
        self.goals = []
        self.start = start_node
        self.path = []
        self.frontier = []
        self.row = ro
        self.col = co
        self.produce_goals()
        self.nodes_produced = 0
        self.nodes_explored = 0

    def is_seen(self, node):
        for n in self.explored:
            if n.queues == node.queues:
                return True
        for n in self.frontier:
            if n.queues == node.queues:
                return True
        return False

    # produces a goal based on start state
    # and then produces other possible goals by the permutation of lines in first goal
    def produce_goals(self):
        letters = {}
        for ro in range(self.row):
            for co in range(self.col):
                if self.start.queues[ro][co] == '#':
                    continue
                if self.start.queues[ro][co][1] in letters.keys():
                    letters[self.start.queues[ro][co][1]].append(self.start.queues[ro][co])
                else:
                    letters[self.start.queues[ro][co][1]] = [self.start.queues[ro][co]]
        goal_queues = []
        for key in letters.keys():
            if len(letters[key]) < self.col:
                l = sorted(letters[key], reverse=True)
                l.insert(0, '#')
                goal_queues.append(l)
            else:
                goal_queues.append(sorted(letters[key], reverse=True))

        self.goals = list(permutations(goal_queues))

    # calculates heuristic for every node in next_nodes list
    # by counting the difference between the node and evey possible goal
    # and choosing the minimum of that as heuristic value
    def heuristic(self, next_nodes):
        min_heuristic = 2 ** (self.row * self.col)
        for node in next_nodes:
            for g in self.goals:
                goal_index = 0
                for ro in range(self.row):
                    for co in range(self.col):
                        if g[ro][co] != node.queues[ro][co]:
                            goal_index += 1
                if goal_index < min_heuristic:
                    min_heuristic = goal_index
            node.h = min_heuristic

    # chooses the node with least cost or least f ( f = h + g )
    def min_cost(self):
        min_cost = 1000000
        best_node = None
        for node in self.frontier:
            if node.h + node.g < min_cost:
                min_cost = node.h + node.g
                best_node = node
        return best_node

    def a_star(self):
        self.frontier.append(self.start)
        self.heuristic(self.frontier)
        while self.frontier:
            node = self.min_cost()
            self.nodes_explored += 1
            for g in self.goals:
                if list(g) == node.queues:
                    self.explored.append(node)
                    return node
            self.frontier.remove(node)
            self.explored.append(node)
            children = node.produce_children()
            self.heuristic(children)
            for child in children:
                if not self.is_seen(child):
                    self.nodes_produced += 1
                    self.frontier.append(child)


# getting input from user
shape = list(map(int, input().split()))
start_queues = []
for i in range(shape[0]):
    start_queues.append(list(input().split()))
start = produce_start_node(start_queues)
my_graph = Graph(start, shape[0], shape[1])
result = my_graph.a_star()

# print path
path = [start.queues]
while result.parent:
    path.insert(0, result.parent.queues)
    result = result.parent
for i in path:
    for line in i:
        print(line)
    print('\n\n')
print('nodes explored', my_graph.nodes_explored)
print('nodes produced', my_graph.nodes_produced)
