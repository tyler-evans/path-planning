import numpy as np
from collections import defaultdict


class SearchNode:

    def __init__(self, rectangle):
        self.rectangle = rectangle
        self.adjacent_nodes = set()

    def add_adjacent(self, other_node):
        self.adjacent_nodes.add(other_node)

        
def A_star(start, goal):

    visited_nodes = []  # for animation

    closed_set = set()
    open_set = {start}

    came_from = dict()

    g_score = defaultdict(lambda: 1e6)
    g_score[start] = 0

    f_score = defaultdict(lambda: 1e6)
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = sorted(open_set, key=lambda node: f_score[node])[0]
        visited_nodes.append(current.rectangle.center)

        if current == goal:
            return reconstruct_path(came_from, current), np.array(visited_nodes)

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in current.adjacent_nodes:
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + dist_between(current, neighbor)

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

    return None, np.array(visited_nodes)


def construct_search_nodes(rectangle_list, initial_rec, goal_rec):
    search_nodes = []
    initial_node, goal_node = None, None

    for rec in rectangle_list:
        node = SearchNode(rec)
        search_nodes.append(node)

        if rec.contains_point(*goal_rec):
            goal_node = node
        if rec.contains_point(*initial_rec):
            initial_node = node

    n = len(search_nodes)
    for i in range(n):
        for j in range(i+1, n):
            node_i = search_nodes[i]
            node_j = search_nodes[j]

            if node_i.rectangle.shares_edge(node_j.rectangle):
                node_i.add_adjacent(node_j)
                node_j.add_adjacent(node_i)

    return search_nodes, initial_node, goal_node


def heuristic(node_0, node_1):
    rec_0 = node_0.rectangle
    rec_1 = node_1.rectangle

    return np.sqrt(np.sum((rec_0.center - rec_1.center) ** 2))


def dist_between(node_0, node_1):
    rec_0 = node_0.rectangle
    rec_1 = node_1.rectangle

    return np.sqrt(np.sum((rec_0.center - rec_1.center) ** 2))


def reconstruct_path(came_from, current):
    total_path = [current.rectangle.center]
    while current in came_from:
        current = came_from[current]
        total_path.append(current.rectangle.center)
    return np.array(total_path)
