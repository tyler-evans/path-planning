import numpy as np

from Environment.Environment import Environment
from Search.RRTSearch import explore_domain
from Utils.DisplayPlot import DisplayPlot, DisplayType


def main():

    problem_size = 100
    num_objects = 20
    min_obj_size, max_obj_size = 10, 50
    max_num_steps = 10000
    step_size = 1
    display_type = DisplayType.ANIMATE

    env = Environment(problem_size, num_objects, min_obj_size, max_obj_size)

    vertices, edges = explore_domain(env.problem, env.initial, env.goal, max_num_steps, step_size=step_size, goal_prob=0.5)

    n = vertices.shape[0]
    path = []
    if n < max_num_steps:
        print('found it!')
        print('number of steps:', n)
        curr_node = edges[n]
        while curr_node != 0:
            path.append(vertices[curr_node])
            curr_node = edges[curr_node]
        path.append(np.array(env.initial)+0.5)
        path.reverse()
        path.append(np.array(env.goal)+0.5)
        path = np.array(path)
    elif n == max_num_steps:
        print('max iterations reached')
    else:
        print('no solution found')

    display = DisplayPlot(display_type, env)
    display.show(vertices, np.array(path))


if __name__ == '__main__':
    main()

