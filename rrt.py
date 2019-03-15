import sys
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import numpy as np
from Environment.Environment import PathPlanningProblem
import random

from Search.RRTSearch import ExploreDomain


def main( argv = None ):

    seed = np.random.randint(4190)
    print('Random seed:', seed)
    random.seed(seed)
    np.random.seed(seed)

    if ( argv == None ):
        argv = sys.argv[1:]

    width = 10.0
    height = 10.0

    pp = PathPlanningProblem( width, height, 10, 4.0, 4.0)
    #pp.obstacles = []
    initial, goals = pp.CreateProblemInstance()

    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_xlim(0.0, width)
    ax.set_ylim(0.0, height)

    for o in pp.obstacles:
        ax.add_patch(o.patch)

    ip = plt.Rectangle((initial[0],initial[1]), 0.1, 0.1, facecolor='#ff0000')
    ax.add_patch(ip)

    for g in goals:
        g = plt.Rectangle((g[0],g[1]), 0.1, 0.1, facecolor='#00ff00')
        ax.add_patch(g)



    num_steps = 5000
    goal = goals[0]
    vertices, edges, images = ExploreDomain(pp, initial, goal, num_steps, ax=ax, goal_prob=0.4)

    images.append(ax.scatter(*vertices.T, s=1))

    n = vertices.shape[0]
    if n < num_steps:
        print('found it!')

        path = []
        curr_node = edges[n]
        while curr_node != 0:
            path.append(vertices[curr_node])
            curr_node = edges[curr_node]
        path.append(np.array(initial))
        path.reverse()
        path.append(np.array(goal))
        path = np.array(path)

        images.append(ax.plot(*path.T, 'r-')[0])
    else:
        print('no solution')


    animation = ArtistAnimation(fig, [images[:i] for i in range(1, len(images)+1)], interval=1, blit=True, repeat=False)
    plt.show()


if ( __name__ == '__main__' ):
    main()

