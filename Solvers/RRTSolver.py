import numpy as np

from Search.RRTSearch import explore_domain
from Utils.DisplayPlot import DisplayPlot


class RRTSolver:

    def __init__(self, env, step_size, max_num_steps, display_type):
        self.env = env
        self.step_size = step_size
        self.max_num_steps = max_num_steps
        self.display_type = display_type
        self.exit_flag = None
        self.path = None

    def solve(self):
        self.vertices, edges = explore_domain(self.env.problem, self.env.initial, self.env.goal, self.max_num_steps,
                                              step_size=self.step_size, goal_prob=0.5)

        n = self.vertices.shape[0]
        path = []
        if n < self.max_num_steps:
            curr_node = edges[n]
            while curr_node != 0:
                path.append(self.vertices[curr_node])
                curr_node = edges[curr_node]
            path.append(np.array(self.env.initial) + 0.5)
            path.reverse()
            path.append(np.array(self.env.goal) + 0.5)
            path = np.array(path)
            self.path = path
        elif n == self.max_num_steps:
            self.exit_flag = 'MAX_ITER_REACHED'

        return self.path

    def show_solution(self):
        display = DisplayPlot(self.display_type, self.env, grid=True)
        display.show(self.vertices, np.array(self.path))
