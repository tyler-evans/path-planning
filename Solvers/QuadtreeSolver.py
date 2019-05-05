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
            initial_center = np.array(self.env.initial)+0.5
            goal_center = np.array(self.env.goal)+0.5
            if self.path.shape[0] > 1:
                self.path[-1] = initial_center
                self.path[0] = goal_center
            else:
                self.path = np.array([initial_center, goal_center])


        return self.path

    def show_solution(self):
        display = DisplayPlot(self.display_type, self.env)
        if self.display_type != DisplayType.NONE:
            self.decomposition.Draw(display.ax)

        display.show(self.vertices, self.path if self.path is not None else np.array([]))
