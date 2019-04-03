import pandas as pd
import random as randy
import numpy as np

from Solvers.QuadtreeSolver import QuadtreeSolver
from Environment.Environment import Environment
from Utils.DataTracker import DataTracker
from Utils.DisplayPlot import DisplayType
from Utils.PathLength import path_length
from Utils.Timer import Timer
from Solvers.RRTSolver import RRTSolver


def main():

    # Environment params
    random_range_start, random_range_end = 111111111, 999999999
    all_num_obstacles = [10, 20, 40, 60]
    maps_per_number_of_obstacles = 10
    goal_bias = 0.5
    problem_size = 100
    min_obj_size = 10
    max_obj_size_map = {10: 50, 20: 50, 40: 20, 60: 10}

    # Quadtree params
    all_decomposition_resolutions = [1.0, 3.0, 5.0]

    # RRT params
    max_num_steps = 100000
    all_step_sizes = [1, 3, 5]

    # Plot/timing params
    # NOTE: only one solution can be shown per environment due to weird matplotlib patch properties
    display_type = DisplayType.NONE

    # Quadtree
    quad_tree_name = 'QUADTREE DECOMPOSITION'
    quad_tree_columns = ['num_objects', 'decomposition_size', 'path_length', 'time']
    quad_tree_display_columns = ["# Objects", "Decomposition Resolution", "Average Path Lengths", "Average Times (Seconds)"]

    quad_tree_results_data_frame = pd.DataFrame(columns=quad_tree_columns)
    quad_tree_data_tracker_table_columns = quad_tree_display_columns
    quad_tree_data_tracker = DataTracker(quad_tree_data_tracker_table_columns, quad_tree_results_data_frame,
                                         problem_size, maps_per_number_of_obstacles, quad_tree_name)

    # RRT
    rrt_name = 'RAPIDLY EXPLORING RANDOM TREE'
    rrt_columns = ['num_objects', 'step_size', 'path_length', 'time']
    rrt_display_columns = ["# Objects", "Step Size", "Path Length", "Run-time (Seconds)"]

    rrt_results_data_frame = pd.DataFrame(columns=rrt_columns)
    rrt_data_tracker_table_columns = rrt_display_columns
    rrt_data_tracker = DataTracker(rrt_data_tracker_table_columns, rrt_results_data_frame,
                                   problem_size, maps_per_number_of_obstacles, rrt_name)

    for num_obstacles in all_num_obstacles:
        max_obj_size = max_obj_size_map[num_obstacles]
        quad_tree_averages_metrics = {}
        rrt_tree_averages_metrics = {}

        for map_number in range(maps_per_number_of_obstacles):

            random_seed = randy.randint(random_range_start, random_range_end)

            # Construct environment
            env = Environment(problem_size, num_obstacles, min_obj_size, max_obj_size, seed=random_seed, display_seed=False)

            # Solve
            for decomposition_resolution in all_decomposition_resolutions:
                if decomposition_resolution not in quad_tree_averages_metrics:
                    quad_tree_averages_metrics[decomposition_resolution] = {}
                    quad_tree_averages_metrics[decomposition_resolution]['path_lengths'] = []
                    quad_tree_averages_metrics[decomposition_resolution]['run_times'] = []
                print('Solving Map: {} - Decomposition Resolution: {}\t({})'.format(env.map_id, decomposition_resolution, quad_tree_name))
                timer = Timer()
                quadtree_solver = QuadtreeSolver(env, decomposition_resolution, display_type)
                path = quadtree_solver.solve()
                timer.end()
                length = path_length(path)
                quad_tree_averages_metrics[decomposition_resolution]['path_lengths'].append(length)
                quad_tree_averages_metrics[decomposition_resolution]['run_times'].append(timer.elapsed_time)
                # quadtree_solver.show_solution()

            for step_size in all_step_sizes:
                if step_size not in rrt_tree_averages_metrics:
                    rrt_tree_averages_metrics[step_size] = {}
                    rrt_tree_averages_metrics[step_size]['path_lengths'] = []
                    rrt_tree_averages_metrics[step_size]['run_times'] = []
                print('Solving Map: {} - Step Size: {}\t({})'.format(env.map_id, step_size, rrt_name))
                timer = Timer()
                rrt_solver = RRTSolver(env, step_size, max_num_steps, display_type, goal_bias=goal_bias)
                path = rrt_solver.solve()
                timer.end()
                length = path_length(path)
                rrt_tree_averages_metrics[step_size]['path_lengths'].append(length)
                rrt_tree_averages_metrics[step_size]['run_times'].append(timer.elapsed_time)
                #rrt_solver.show_solution()

        for key, val in quad_tree_averages_metrics.items():
            quad_tree_data_tracker.results_data_frame = update_results(quad_tree_data_tracker.results_data_frame, num_obstacles, key, np.average(val['path_lengths']), np.average(val['run_times']))

        for key, val in rrt_tree_averages_metrics.items():
            rrt_data_tracker.results_data_frame = update_results(rrt_data_tracker.results_data_frame, num_obstacles, key, np.average(val['path_lengths']), np.average(val['run_times']))

    print("\n{}\n".format(quad_tree_data_tracker))
    print("{}\n".format(rrt_data_tracker))

def update_results(results, *args):
    return results.append({col: val for col, val in zip(results.columns, args)}, ignore_index=True)


if __name__ == '__main__' :
    main()
