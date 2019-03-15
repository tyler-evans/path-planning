import numpy as np

from Environment.Environment import Rectangle


def explore_domain(domain, initial, goal, num_steps, goal_prob=0.5, step_size=0.1, ax=None):

    vertices = np.zeros((num_steps, 2))
    vertices[0] = np.array(initial)
    edges = dict()

    images = []

    for i in range(1, num_steps):

        sample_point = np.random.uniform(0, domain.width, size=2)
        if np.random.rand() < goal_prob:
            sample_point = goal

        nearest_neighbor_idx = np.argmin(np.sum((vertices[:i] - sample_point)**2, axis=1))
        nearest_neighbor = vertices[nearest_neighbor_idx]

        direction = sample_point - nearest_neighbor
        direction /= np.linalg.norm(direction)

        new_point = nearest_neighbor + step_size*direction
        new_point = np.clip(new_point, 0.0, domain.width)

        rec = Rectangle(*new_point, 0.1, 0.1)
        if not domain.check_overlap(rec):
            vertices[i] = new_point
            edges[i] = nearest_neighbor_idx

            if ax:
                images.append(ax.scatter(*new_point, color='r', s=1))

            if np.linalg.norm(goal - new_point) < step_size:  # found it
                return vertices[:i], edges, images
        else:
            vertices[i] = nearest_neighbor

    return vertices, edges, images
