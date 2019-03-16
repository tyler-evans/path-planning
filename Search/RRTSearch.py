import numpy as np

from Environment.Environment import Rectangle


def explore_domain(domain, initial, goal, num_steps, goal_prob=0.5, step_size=0.1):

    vertices = np.zeros((num_steps, 2))
    vertices[0] = np.array(initial)
    edges = dict()

    for i in range(1, num_steps):
        sample_point = np.random.uniform(domain.problem_size, size=2) if np.random.rand() >= goal_prob else goal

        nearest_neighbor_idx = np.argmin(np.sum((vertices[:i] - sample_point)**2, axis=1))
        nearest_neighbor = vertices[nearest_neighbor_idx]

        direction = normalize(sample_point - nearest_neighbor)
        new_point = np.clip(nearest_neighbor + step_size*direction, 0, domain.problem_size)

        if not domain.check_overlap(Rectangle(*new_point, 0.1, 0.1)):
            vertices[i] = new_point
            edges[i] = nearest_neighbor_idx

            if np.linalg.norm(goal - new_point) < step_size:  # found it
                return vertices[:i], edges
        else:
            vertices[i] = nearest_neighbor

    return vertices, edges


def normalize(vec):
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else 0


def closest_basis_direction(vec):
    return normalize(np.abs(vec) > (np.sqrt(2)/2)) * np.sign(vec)


def distance_to_graph(point, vertices, num_vertices):
    return np.linalg.norm(point - vertices[np.argmin(np.sum((vertices[:num_vertices] - point) ** 2, axis=1))])


# TODO: experimental
def explore_domain_with_basis_fallback(domain, initial, goal, num_steps, goal_prob=0.5, step_size=0.1):

    vertices = np.zeros((num_steps, 2))
    vertices[0] = np.array(initial)
    edges = dict()

    for i in range(1, num_steps):
        sample_point = np.random.uniform(domain.problem_size, size=2) if np.random.rand() >= goal_prob else goal

        nearest_neighbor_idx = np.argmin(np.sum((vertices[:i] - sample_point)**2, axis=1))
        nearest_neighbor = vertices[nearest_neighbor_idx]

        for direction in [normalize(sample_point - nearest_neighbor), (1,0), (0,1), (-1,0), (0,-1)]:
            direction = np.array(direction)

            if i-1 in edges:
                prev_dir = closest_basis_direction(vertices[edges[i-1]] - nearest_neighbor)
                if (direction == prev_dir).all():
                    continue

            new_point = nearest_neighbor + step_size*direction
            new_point = np.clip(new_point, 0, domain.problem_size)

            if distance_to_graph(new_point, vertices, i) < step_size/2.0 and np.any(sample_point != goal):
                continue

            if not domain.check_overlap(Rectangle(*new_point, 0.1, 0.1)):
                vertices[i] = new_point
                edges[i] = nearest_neighbor_idx

                if np.linalg.norm(goal - new_point) < step_size:  # found it
                    return vertices[:i], edges

                break
            else:
                vertices[i] = nearest_neighbor

    return vertices, edges
