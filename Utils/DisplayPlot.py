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

    def show(self, vertices, path):
        if self.grid:
            ticks = np.arange(0, self.env.width+1, 1)
            self.env.ax.set_xticks(ticks, minor=True)
            self.env.ax.set_yticks(ticks, minor=True)
            plt.grid(which='minor', alpha=0.4)

        if self.display_type == DisplayType.ANIMATE:
            images = [self.env.ax.scatter(*vertex, color='r', s=1) for vertex in vertices]
            images.append(self.env.ax.scatter(*vertices.T, s=1))
            images.append(self.env.ax.plot(*path.T, 'r-')[0])
            animation = ArtistAnimation(self.env.fig, [images[:i] for i in range(1, len(images) + 1)], interval=0.01,
                                        blit=True, repeat=False)
            plt.show()
        elif self.display_type == DisplayType.PLOT:
            self.env.ax.scatter(*vertices.T, color='k', s=1)
            self.env.ax.plot(*path.T, 'r-')
            plt.show()


