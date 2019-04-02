import pandas as pd

from Solvers.QuadtreeSolver import QuadtreeSolver
from Environment.Environment import Environment
from Utils.DisplayPlot import DisplayType
from Utils.PathLength import path_length
from Utils.Timer import Timer
from Solvers.RRTSolver import RRTSolver


def main():

    # Environment params
    problem_size = 100
    num_objects = 10
    min_obj_size = 10
    max_obj_size_map = {10: 50, 20: 50, 40: 20, 60: 10}

    # Quadtree params
    decomposition_resolution = 1.0

    # RRT params
    max_num_steps = 10000
    step_size = 1 # 1-5

    # Plot/timing params
    # NOTE: only one solution can be shown per environment due to weird matplotlib patch properties
    display_type = DisplayType.NONE

    results = pd.DataFrame(columns=['map_id', 'num_objects', 'algorithm', 'path_length', 'time'])

    for num_objects in [10, 20, 40, 60]:
        max_obj_size = max_obj_size_map[num_objects]

        # Construct environment
        env = Environment(problem_size, num_objects, min_obj_size, max_obj_size)
        print('Solving map: ', env.map_id)

        # Solve
        timer = Timer()
        quadtree_solver = QuadtreeSolver(env, decomposition_resolution, display_type)
        path = quadtree_solver.solve()
        timer.end()
        length = path_length(path)
        #quadtree_solver.show_solution()
        results = update_results(results, env.map_id, num_objects, 'Quadtree', length, timer.elapsed_time)

        timer = Timer()
        rrt_solver = RRTSolver(env, step_size, max_num_steps, display_type)
        path = rrt_solver.solve()
        timer.end()
        length = path_length(path)
        #rrt_solver.show_solution()
        results = update_results(results, env.map_id, num_objects, 'RRT', length, timer.elapsed_time)


    print(results)


def update_results(results, *args):
    return results.append({col: val for col, val in zip(results.columns, args)}, ignore_index=True)


if __name__ == '__main__' :
    main()
