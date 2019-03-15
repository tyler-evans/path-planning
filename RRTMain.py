import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import numpy as np
from Environment.Environment import Environment

from Search.RRTSearch import ExploreDomain


def main():

    width = 10.0
    height = 10.0
    num_objects = 10
    max_num_steps = 5000

    env = Environment(width, height, num_objects, 4.0, 4.0)

    vertices, edges, images = ExploreDomain(env.problem, env.initial, env.goal, max_num_steps, goal_prob=0.5, ax=env.ax)

    images.append(env.ax.scatter(*vertices.T, s=1))

    n = vertices.shape[0]
    if n < max_num_steps:
        print('found it!')

        path = []
        curr_node = edges[n]
        while curr_node != 0:
            path.append(vertices[curr_node])
            curr_node = edges[curr_node]
        path.append(np.array(env.initial))
        path.reverse()
        path.append(np.array(env.goal))
        path = np.array(path)

        images.append(env.ax.plot(*path.T, 'r-')[0])
    else:
        print('no solution')

    animation = ArtistAnimation(env.fig, [images[:i] for i in range(1, len(images)+1)], interval=1, blit=True, repeat=False)
    plt.show()


if __name__ == '__main__':
    main()

