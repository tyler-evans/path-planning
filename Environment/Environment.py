import matplotlib.pyplot as plt
import numpy as np

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
        return any([
            self.contains_point(rec.x, rec.y),
            self.contains_point(rec.x+rec.width, rec.y),
            self.contains_point(rec.x, rec.y+rec.height),
            self.contains_point(rec.x+rec.width, rec.y+rec.height)
        ])

    def contains_point(self, x, y):
        return all([
            self.x <= x,
            x <= self.x + self.width,
            self.y <= y,
            y <= self.y + self.height
        ])


class Obstacle(Rectangle):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(x, y, width, height)
        self.color = color
        if color is not None:
            self.patch = plt.Rectangle((self.x, self.y), self.width, self.height, facecolor=color, edgecolor='#202020',
                                       alpha=0.6)


class PathPlanningProblem:
    def __init__(self, problem_size, num_objects, min_obj_size, max_obj_size):
        self.problem_size = problem_size
        self.width = problem_size
        self.height = problem_size
        self.obstacles = self.create_obstacles(num_objects, min_obj_size, max_obj_size)

    def create_obstacles(self, num_objects, min_obj_size, max_obj_size):
        obstacles = []

        while len(obstacles) < num_objects:
            x = np.random.randint(self.width)
            y = np.random.randint(self.height)
            w = np.random.randint(min_obj_size, max_obj_size+1)
            h = np.random.randint(min_obj_size, max_obj_size+1)
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
            ix = np.random.randint(1, self.width)
            iy = np.random.randint(1, self.height)

            oinitial = Obstacle(ix, iy, 0.1, 0.1)
            found = True
            for obs in self.obstacles:
                if oinitial.calculate_overlap(obs) > 0.0:
                    found = False
                    break

        found = False
        while not found:
            gx = np.random.randint(1, self.width)
            gy = np.random.randint(1, self.height)

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

    map_id = 1

    def __init__(self, problem_size, num_objects, min_obj_size, max_obj_size, grid=True, seed=None, display_seed=True):

        Seed(seed, display_seed)
        self.map_id = Environment.map_id
        Environment.map_id += 1

        self.seed = seed

        self.width = problem_size
        self.height = problem_size
        self.num_objects = num_objects
        self.min_object_size = min_obj_size
        self.max_object_size = max_obj_size

        self.problem = PathPlanningProblem(problem_size, num_objects, min_obj_size, max_obj_size)
        self.initial, self.goal = self.problem.create_problem_instance()
