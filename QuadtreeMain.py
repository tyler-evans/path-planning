import matplotlib.pyplot as plt
import numpy as np

from CellDecomposition.CellDecomposition import QuadTreeDecomposition
from Search.AStarSearch import construct_search_nodes, A_star

from Environment.Environment import Environment


def main():

    width = 10.0
    height = 10.0
    num_objects = 15
    decomposition_resolution = 0.1

    env = Environment(width, height, num_objects, 3.0, 3.0)

    decomposition = QuadTreeDecomposition(env.problem, decomposition_resolution)
    decomposition.Draw(env.ax)

    free_nodes = decomposition.get_leaf_nodes(decomposition.root)
    search_nodes, initial_node, goal_node = construct_search_nodes(free_nodes, env.initial, env.goal)

    #ax.scatter(initial_node.rectangle.center_x, initial_node.rectangle.center_y, color='#00ff00', s=1)
    #ax.scatter(goal_node.rectangle.center_x, goal_node.rectangle.center_y, color='#00ff00', s=1)

    if not(initial_node and goal_node):
        print('bad initial or goal nodes (spawned on mixed tile)')
        exit(1)

    print('solving...', end=' ')
    path, visited = A_star(initial_node, goal_node)
    print('done!')
    if path is None:
        print('no solution!')

    for node in visited:
        rec = node.rectangle
        env.ax.scatter(rec.center_x, rec.center_y, color='k', s=1, alpha=1.0)
        plt.pause(0.001)

    path_coords = np.array([node.rectangle.center for node in path])
    env.ax.plot(*path_coords.T, 'r-')

    plt.show()


if __name__ == '__main__' :
    main()


