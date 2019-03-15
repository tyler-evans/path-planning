import matplotlib.pyplot as plt

from CellDecomposition.CellDecomposition import QuadTreeDecomposition
from Search.AStarSearch import construct_search_nodes, A_star
from Environment.Environment import Environment
from Utils.DisplayPlot import DisplayPlot, DisplayType


def main():

    problem_size = 100
    num_objects = 10
    min_obj_size, max_obj_size = 10, 50
    decomposition_resolution = 1.0
    display_type = DisplayType.ANIMATE

    env = Environment(problem_size, num_objects, min_obj_size, max_obj_size, grid=False)

    decomposition = QuadTreeDecomposition(env.problem, decomposition_resolution)
    decomposition.Draw(env.ax)

    free_nodes = decomposition.get_leaf_nodes(decomposition.root)
    search_nodes, initial_node, goal_node = construct_search_nodes(free_nodes, env.initial, env.goal)

    if not(initial_node and goal_node):
        print('bad initial or goal nodes (spawned on mixed tile)')
        plt.show()
        exit(1)

    print('solving...', end=' ')
    path, vertices = A_star(initial_node, goal_node)
    if path is None:
        print('no solution!')
    else:
        print('solution found!')
        display = DisplayPlot(display_type, env)
        display.show(vertices, path)


if __name__ == '__main__' :
    main()


