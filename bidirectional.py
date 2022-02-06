from typing import List
import numpy as np
import re
from copy import copy, deepcopy
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
    return Node(start_q, square)


class Node:
    def __init__(self, queues, square):
        self.nextNodes = []
        self.queues = queues
        self.square = square
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
            ch = Node(q, s)
            ch.parent = self
            self.nextNodes.append(ch)
        return self.nextNodes


class Graph:

    def __init__(self, start: Node, row, col):
        self.goal = Node([[0]], (0, 0))  # made up final state
        self.explored = []
        self.Qi: List[Node] = []  # frontier for bfs starting from start state
        self.Qg: List[Node] = []  # frontier for bfs starting from final state
        self.goals = []
        self.start = start
        self.row = row
        self.col = col
        self.produce_goals()
        self.nodes_produced = 0
        self.nodes_explored = 0

    def is_seen(self, node, array: List[Node]):
        for n in array:
            if n.queues == node.queues:
                return n
        return False

    def produce_goals(self):
        letters = {}
        for r in range(self.row):
            for c in range(self.col):
                if self.start.queues[r][c] == '#':
                    continue
                if self.start.queues[r][c][1] in letters.keys():
                    letters[self.start.queues[r][c][1]].append(self.start.queues[r][c])
                else:
                    letters[self.start.queues[r][c][1]] = [self.start.queues[r][c]]
        goal_queues = []
        for key in letters.keys():
            if len(letters[key]) < self.col:
                l = sorted(letters[key], reverse=True)
                l.insert(0, '#')
                goal_queues.append(l)
            else:
                goal_queues.append(sorted(letters[key], reverse=True))
        goals_perm = list(permutations(goal_queues))
        for i in goals_perm:
            for r in range(self.row):
                if i[r][0] == '#':
                    s = (r, 0)
                    g = Node(list(i), s)
                    g.nextNodes.append(self.goal)
                    self.goals.append(g)
        self.goal.nextNodes = self.goals

    def bidirectional(self):
        self.Qi.append(self.start)
        self.Qg.append(self.goal)
        self.explored.append(self.start)
        self.explored.append(self.goal)
        while self.Qg and self.Qi:
            # bfs from start state
            xi = self.Qi.pop(0)
            xi.produce_children()
            self.nodes_explored += 1
            self.explored.append(xi)
            xi_in_Qg = self.is_seen(xi, self.Qg)
            if xi_in_Qg:
                return xi_in_Qg, xi
            xi_in_goals = self.is_seen(xi, self.goal.nextNodes)
            if xi_in_goals:
                return xi_in_goals, xi
            for node in xi.nextNodes:
                n = self.is_seen(node, self.explored)
                if not n:
                    self.Qi.append(node)
                    self.nodes_produced += 1

            # bfs from final state
            xg = self.Qg.pop(0)
            self.nodes_explored += 1
            self.explored.append(xg)
            self.nodes_produced += len(xg.nextNodes)
            if xg != self.goal:
                xg.produce_children()
            xg_in_Qi = self.is_seen(xg, self.Qi)
            if xg_in_Qi:
                return xg, xg_in_Qi
            xg_in_start = self.is_seen(xg, [self.start])
            if xg_in_start:
                return xg, xg_in_start
            for node in xg.nextNodes:
                if not self.is_seen(node, self.explored):
                    self.Qg.append(node)
                    self.nodes_produced += 1
        return False

    def is_goal(self, node):
        for g in self.goals:
            if g == node.queues:
                return True
            return False


shape = list(map(int, input().split()))

start_queues = []
for i in range(shape[0]):
    start_queues.append(list(input().split()))

start = produce_start_node(start_queues)
my_graph = Graph(start, shape[0], shape[1])
# print path
node_Qg, node_Qi = my_graph.bidirectional()
path = []
while node_Qi.parent:
    path.insert(0, node_Qi.parent)
    node_Qi = node_Qi.parent
path.append(node_Qg)
while node_Qg.parent:
    path.append(node_Qg.parent)
    node_Qg = node_Qg.parent

for i in path:
    for line in i.queues:
        print(line)
    print('\n')
print('nodes explored', my_graph.nodes_explored)
print('nodes produced', my_graph.nodes_produced)
