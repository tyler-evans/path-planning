import matplotlib.pyplot as plt
import numpy as np
import random

from Utils.Seed import Seed


class Rectangle:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center_x = x + 0.5 * width
        self.center_y = y + 0.5 * height
        self.center = np.array([self.center_x, self.center_y])

    def calculate_x_overlap(self, obs):
        min = np.min((self.x, obs.x))
        max = np.max((obs.x + obs.width, self.x + self.width))
        return (max - min) - (self.width + obs.width)

    def calculate_y_overlap(self, obs):
        min = np.min((self.y, obs.y))
        max = np.max((obs.y + obs.height, self.y + self.height))
        return (max - min) - (self.height + obs.height)

    def calculate_overlap(self, obs):
        overlapX = self.calculate_x_overlap(obs)
        overlapY = self.calculate_y_overlap(obs)

        if (overlapX < 0) and (overlapY < 0):
            overlap = overlapX * overlapY
        else:
            overlap = 0.0

        return overlap

    def shares_edge(self, rec):
        overlapX = self.calculate_x_overlap(rec)
        overlapY = self.calculate_y_overlap(rec)

        share_vertical_edge = (overlapX == 0) and (overlapY < 0)
        share_horizontal_edge = (overlapY == 0) and (overlapX < 0)

        return share_vertical_edge or share_horizontal_edge

    def contains_point(self, x, y):
        return all([self.x <= x,
                    x < self.x + self.width,
                    self.y <= y,
                    y < self.y + self.height])


class Obstacle(Rectangle):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(x, y, width, height)
        self.color = color
        if color is not None:
            self.patch = plt.Rectangle((self.x, self.y), self.width, self.height, facecolor=color, edgecolor='#202020',
                                       alpha=0.6)


class PathPlanningProblem:
    def __init__(self, width, height, onum, owidth, oheight):
        self.width = width
        self.height = height
        self.obstacles = self.create_obstacles(onum, owidth, oheight)

    def create_obstacles(self, onum, owidth, oheight):
        obstacles = []

        while len(obstacles) < onum:
            x = random.uniform(0.0, self.width)
            y = random.uniform(0.0, self.height)
            w = random.uniform(0.1, owidth)
            h = random.uniform(0.1, oheight)
            if (x + w) > self.width:
                w = self.width - x
            if (y + h) > self.height:
                h = self.height - y
            obs = Obstacle(x, y, w, h, '#808080')
            found = False
            for o in obstacles:
                if o.calculate_overlap(obs) > 0.0:
                    found = True
                    break
            if not found:
                obstacles = obstacles + [obs]
        return obstacles

    def create_problem_instance(self):
        found = False
        while not found:
            ix = random.uniform(0.0, self.width)
            iy = random.uniform(0.0, self.height)

            oinitial = Obstacle(ix, iy, 0.1, 0.1)
            found = True
            for obs in self.obstacles:
                if oinitial.calculate_overlap(obs) > 0.0:
                    found = False
                    break

        found = False
        while not found:
            gx = random.uniform(0.0, self.width)
            gy = random.uniform(0.0, self.height)

            ogoal = Obstacle(gx, gy, 0.1, 0.1)
            found = True
            for obs in self.obstacles:
                if ogoal.calculate_overlap(obs) > 0.0:
                    found = False
                    break
            if oinitial.calculate_overlap(ogoal) > 0.0:
                found = False

        return (ix, iy), (gx, gy)

    def check_overlap(self, r):
        overlap = False
        for o in self.obstacles:
            if r.calculate_overlap(o) > 0:
                overlap = True
                break
        return overlap

    def calculate_coverage(self, path, dim):
        x = np.arange(0.0, self.width, dim)
        y = np.arange(0.0, self.height, dim)
        counts = np.zeros((len(y), len(x)))
        for p in path:
            i = int(p[1] / dim)
            j = int(p[0] / dim)
            counts[j][i] = counts[j][i] + 1
        return x, y, counts


class Environment:

    def __init__(self, width, height, num_objects, min_object_size, max_object_size, seed=None):

        Seed(seed)

        self.width = width
        self.height = height
        self.num_objects = num_objects
        self.min_object_size = min_object_size
        self.max_object_size = max_object_size

        # TODO accept min and max object sizes
        self.problem = PathPlanningProblem(width, height, self.num_objects, self.max_object_size, self.max_object_size)
        self.initial, self.goal = self.problem.create_problem_instance()

        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xlim(0.0, width)
        self.ax.set_ylim(0.0, height)

        for o in self.problem.obstacles:
            self.ax.add_patch(o.patch)

        ip = plt.Rectangle((self.initial[0], self.initial[1]), 0.1, 0.1, facecolor='#ff0000')
        self.ax.add_patch(ip)

        g = plt.Rectangle((self.goal[0], self.goal[1]), 0.1, 0.1, facecolor='#00ff00')
        self.ax.add_patch(g)
