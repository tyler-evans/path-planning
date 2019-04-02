from Solvers.QuadtreeSolver import QuadtreeSolver
from Environment.Environment import Environment
from Utils.DisplayPlot import DisplayType
from Solvers.RRTSolver import RRTSolver


def main():

    # Environment params
    problem_size = 100
    num_objects = 10
    min_obj_size, max_obj_size = 10, 50

    # Quadtree params
    decomposition_resolution = 1.0

    # RRT params
    max_num_steps = 10000
    step_size = 1

    # Plot/timing params
    display_type = DisplayType.PLOT

    # Construct environment
    env = Environment(problem_size, num_objects, min_obj_size, max_obj_size)

    # Solve
    quadtree_solver = QuadtreeSolver(env, decomposition_resolution, display_type)
    path = quadtree_solver.solve()
    quadtree_solver.show_solution()

    rrt_solver = RRTSolver(env, step_size, max_num_steps, display_type)
    path = rrt_solver.solve()
    rrt_solver.show_solution()


if __name__ == '__main__' :
    main()
