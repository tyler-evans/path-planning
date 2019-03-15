from CellDecomposition.CellDecomposition import QuadTreeDecomposition


import sys
import matplotlib.pyplot as plt
import numpy as np
import copy
import random

from Environment.Environment import PathPlanningProblem
from Search.AStarSearch import construct_search_nodes, A_star

def main( argv = None ):

    if ( argv == None ):
        argv = sys.argv[1:]

    seed = np.random.randint(4190)
    print('Random seed:', seed)
    random.seed(seed)
    np.random.seed(seed)

    width = 10.0
    height = 10.0

    pp = PathPlanningProblem( width, height, 15, 3.0, 3.0)
    initial, goals = pp.CreateProblemInstance()
    goal = goals[0]

    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_xlim(0.0, width)
    ax.set_ylim(0.0, height)

    for o in pp.obstacles:
        ax.add_patch(copy.copy(o.patch) )
    ip = plt.Rectangle((initial[0],initial[1]), 0.1, 0.1, facecolor='#ff0000')
    ax.add_patch(ip)

    for g in goals:
        g = plt.Rectangle((g[0],g[1]), 0.1, 0.1, facecolor='#00ff00')
        ax.add_patch(g)

    qtd = QuadTreeDecomposition(pp, 0.1) # 0.2
    qtd.Draw(ax)
    n = qtd.CountCells()
    ax.set_title('Quadtree Decomposition\n{0} cells'.format(n))

    free_nodes = qtd.get_leaf_nodes(qtd.root)

    search_nodes, initial_node, goal_node = construct_search_nodes(free_nodes, initial, goal)
    ax.scatter(initial_node.rectangle.center_x, initial_node.rectangle.center_y, color='#00ff00', s=1)
    ax.scatter(goal_node.rectangle.center_x, goal_node.rectangle.center_y, color='#00ff00', s=1)

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
        ax.scatter(rec.center_x, rec.center_y, color='k', s=1, alpha=1.0)
        plt.pause(0.001)

    path_coords = np.array([node.rectangle.center for node in path])
    ax.plot(*path_coords.T, 'r-')

    plt.show()


if ( __name__ == '__main__' ):
    main()


