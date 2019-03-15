import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import numpy as np
from Environment.Environment import Environment

from Search.RRTSearch import ExploreDomain


def main():

    width = 10.0
    height = 10.0
    num_objects = 10

    environment = Environment(width, height, num_objects, 4.0, 4.0)
    pp = environment.problem
    initial, goal = environment.initial, environment.goal
    ax = environment.ax
    fig = environment.fig

    num_steps = 5000
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


if  __name__ == '__main__':
    main()

