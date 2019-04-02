import pandas as pd
import random as randy

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
    all_num_obstacles = [1, 2, 4, 6]
    maps_per_number_of_obstacles = 1
    problem_size = 100
    min_obj_size = 10
    max_obj_size_map = {1: 50, 2: 50, 4: 20, 6: 10}

    # Quadtree params
    all_decomposition_resolutions = [1.0, 3.0, 5.0]

    # RRT params
    max_num_steps = 10000
    all_step_sizes = [1, 3, 5]

    # Plot/timing params
    # NOTE: only one solution can be shown per environment due to weird matplotlib patch properties
    display_type = DisplayType.NONE

    # Quadtree
    quad_tree_name = 'Quadtree Decomposition'
    quad_tree_columns = ['map_id', 'num_objects', 'decomposition_size', 'path_length', 'time']
    quad_tree_display_columns = ["Map Number", "# Objects", "Decomposition Resolution", "Path Length", "Run-time (Seconds)"]

    quad_tree_results_data_frame = pd.DataFrame(columns=quad_tree_columns)
    quad_tree_data_tracker_table_columns = quad_tree_display_columns
    quad_tree_data_tracker = DataTracker(quad_tree_data_tracker_table_columns, quad_tree_results_data_frame,
                                         problem_size, display_plot_name=quad_tree_name)

    # RRT
    rrt_name = 'Rapidly Exploring Random Tree'
    rrt_columns = ['map_id', 'num_objects', 'step_size', 'path_length', 'time']
    rrt_display_columns = ["Map Number", "# Objects", "Step Size", "Path Length", "Run-time (Seconds)"]

    rrt_results_data_frame = pd.DataFrame(columns=rrt_columns)
    rrt_data_tracker_table_columns = rrt_display_columns
    rrt_data_tracker = DataTracker(rrt_data_tracker_table_columns, rrt_results_data_frame,
                                   problem_size, display_plot_name=rrt_name)

    for num_obstacles in all_num_obstacles:
        max_obj_size = max_obj_size_map[num_obstacles]

        for map_number in range(maps_per_number_of_obstacles):

            random_seed = randy.randint(random_range_start, random_range_end)

            # Construct environment
            env = Environment(problem_size, num_obstacles, min_obj_size, max_obj_size, seed=random_seed, display_seed=False)

            # Solve
            for decomposition_resolution in all_decomposition_resolutions:
                print('Solving Map: {} - Decomposition Resolution: {}\t(Quadtree Decomposition)'.format(env.map_id, decomposition_resolution))
                timer = Timer()
                quadtree_solver = QuadtreeSolver(env, decomposition_resolution, display_type)
                path = quadtree_solver.solve()
                timer.end()
                length = path_length(path)
                # quadtree_solver.show_solution()
                quad_tree_data_tracker.results_data_frame = update_results(quad_tree_data_tracker.results_data_frame, env.map_id, num_obstacles, decomposition_resolution, length, timer.elapsed_time)

            for step_size in all_step_sizes:
                print('Solving Map: {} - Step Size: {}\t(Rapidly Exploring Random Tree)'.format(env.map_id, step_size))
                timer = Timer()
                rrt_solver = RRTSolver(env, step_size, max_num_steps, display_type)
                path = rrt_solver.solve()
                timer.end()
                length = path_length(path)
                #rrt_solver.show_solution()
                rrt_data_tracker.results_data_frame = update_results(rrt_data_tracker.results_data_frame, env.map_id, num_obstacles, step_size, length, timer.elapsed_time)

    print("\n{}\n".format(quad_tree_data_tracker))
    print("{}\n".format(rrt_data_tracker))

def update_results(results, *args):
    return results.append({col: val for col, val in zip(results.columns, args)}, ignore_index=True)


if __name__ == '__main__' :
    main()
