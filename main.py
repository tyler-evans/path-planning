import pandas as pd
import random as randy

from Utils.Seed import Seed
from Solvers.QuadtreeSolver import QuadtreeSolver
from Environment.Environment import Environment
from Utils.DataTracker import DataTracker
from Utils.DisplayPlot import DisplayType
from Utils.PathLength import path_length
from Utils.Timer import Timer
from Solvers.RRTSolver import RRTSolver


def main():

    goal_bias = 0.5
    problem_size = 100
    min_obj_size = 10

    decomposition_resolution = 1.0
    step_size = 1.0
    max_num_steps = 10000

    display_type = DisplayType.ANIMATE

    random_seed = 158328151
    num_obstacles = 40
    max_obj_size = 10

    Seed(random_seed)
    env = Environment(problem_size, num_obstacles, min_obj_size, max_obj_size, seed=random_seed, display_seed=False)
    timer = Timer()
    quadtree_solver = QuadtreeSolver(env, decomposition_resolution, display_type)
    path = quadtree_solver.solve()
    timer.end()
    print('Length: ', path_length(path))
    print('Time: ', timer.elapsed_time)
    quadtree_solver.show_solution()

    Seed(random_seed)
    env = Environment(problem_size, num_obstacles, min_obj_size, max_obj_size, seed=random_seed, display_seed=False)
    timer = Timer()
    rrt_solver = RRTSolver(env, step_size, max_num_steps, display_type, goal_bias=goal_bias)
    path = rrt_solver.solve()
    timer.end()
    print('Length: ', path_length(path))
    print('Time: ', timer.elapsed_time)
    rrt_solver.show_solution()


if __name__ == '__main__' :
    main()
