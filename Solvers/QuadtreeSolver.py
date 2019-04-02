import numpy as np

from CellDecomposition.CellDecomposition import QuadTreeDecomposition
from Search.AStarSearch import construct_search_nodes, A_star
from Utils.DisplayPlot import DisplayPlot, DisplayType


class QuadtreeSolver:

    def __init__(self, env, decomposition_resolution, display_type):
        self.env = env
        self.display_type = display_type
        self.path = None
        self.decomposition = QuadTreeDecomposition(env.problem, decomposition_resolution)

        free_nodes = self.decomposition.get_leaf_nodes(self.decomposition.root)
        search_nodes, self.initial_node, self.goal_node = construct_search_nodes(free_nodes, env.initial, env.goal)

    def solve(self):
        self.path, self.vertices = A_star(self.initial_node, self.goal_node)

        if self.path is not None:
            a, b = np.array(self.env.goal), np.array(self.env.initial)
            self.path = np.vstack([a + 0.5, self.path, b + 0.5])

        return self.path

    def show_solution(self):
        display = DisplayPlot(self.display_type, self.env)
        if self.display_type != DisplayType.NONE:
            self.decomposition.Draw(self.env.ax)

        display.show(self.vertices, self.path if self.path is not None else np.array([]))
