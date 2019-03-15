import sys
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import numpy as np
from pathplanning import PathPlanningProblem, Rectangle
import random



def ExploreDomain( domain, initial, goal, num_steps, ax=None, goal_prob=0.5, step_size=0.1):

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
        if not domain.CheckOverlap(rec):
            vertices[i] = new_point
            edges[i] = nearest_neighbor_idx

            if ax:
                images.append(ax.scatter(*new_point, color='r', s=1))
                #plt.pause(0.0001)

            if np.linalg.norm(goal - new_point) < step_size:
                return vertices[:i], edges, images
        else:
            vertices[i] = nearest_neighbor

    return vertices, edges, images


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
    vertices, edges, images = ExploreDomain( pp, initial, goal, num_steps, ax=ax, goal_prob=0.4)

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




#     ax = fig.add_subplot(1,2,2)
# #    x,y,z = pp.CalculateCoverage(path, 0.5)
#
# #    X,Y = np.meshgrid(x,y)
# #    Z = z
# #    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.coolwarm)
#
#     heatmap, x, y = np.histogram2d(path[:,0], path[:,1], bins = 50, range=[[0.0, pp.width], [0.0, pp.height]])
#     coverage = float( np.count_nonzero(heatmap) ) / float( len(heatmap) * len(heatmap[0]))
#     extent = [ x[0], x[-1], y[0], y[-1]]
#     ax.set_title('Random Walk\nCoverage {0}'.format(coverage))
#     plt.imshow(np.rot90(heatmap))
#     plt.colorbar()
#
#     plt.show()

if ( __name__ == '__main__' ):
    main()

