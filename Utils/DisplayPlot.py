from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import ArtistAnimation


class DisplayType(Enum):
    ANIMATE = 1
    PLOT = 2
    NONE = 3


class DisplayPlot:

    def __init__(self, display_type, env, grid=False):
        self.display_type = display_type
        self.env = env
        self.grid = grid

        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xlim(0.0, env.width)
        self.ax.set_ylim(0.0, env.height)

        for o in env.problem.obstacles:
            self.ax.add_patch(o.patch)

        ip = plt.Rectangle((env.initial[0], env.initial[1]), 1.0, 1.0, facecolor='#ff0000')
        self.ax.add_patch(ip)

        g = plt.Rectangle((env.goal[0], env.goal[1]), 1.0, 1.0, facecolor='#00ff00')
        self.ax.add_patch(g)

    def show(self, vertices, path):
        if self.grid:
            ticks = np.arange(0, self.env.width+1, 1)
            self.ax.set_xticks(ticks, minor=True)
            self.ax.set_yticks(ticks, minor=True)
            plt.grid(which='minor', alpha=0.4)

        if self.display_type == DisplayType.ANIMATE:
            images = [self.ax.scatter(*vertex, color='r', s=1) for vertex in vertices]
            images.append(self.ax.scatter(*vertices.T, s=1))
            if path is not None and path.shape[0] > 0:
                images.append(self.ax.plot(*path.T, 'r-')[0])
                print('Animating...')
                animation = ArtistAnimation(self.fig, [images[:i] for i in range(1, len(images) + 1)], interval=1.0,
                                            blit=True, repeat=False)
            #animation.save('Plots/map_%d.gif'%self.env.map_id, writer='imagemagick')
            input('ready')
            plt.show()
            print('Done')
        elif self.display_type == DisplayType.PLOT:
            self.ax.scatter(*vertices.T, color='k', s=1)
            if path is not None and path.shape[0] > 0:
                self.ax.plot(*path.T, 'r-')
            #plt.savefig('Plots/map_%d_seed_%d.png'%(self.env.map_id, self.env.seed))
            input('ready')
            plt.show()
            print('Done')



