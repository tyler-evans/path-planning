__author__ = 'Jacky Baltes <jacky@cs.umanitoba.ca>'

import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import copy
import random
from collections import defaultdict
from pathplanning import PathPlanningProblem, Rectangle

from matplotlib.animation import FuncAnimation


class SearchNode:

    def __init__(self, rectangle):
        self.rectangle = rectangle
        self.adjacent_nodes = set()

    def add_adjacent(self, other_node):
        self.adjacent_nodes.add(other_node)


class CellDecomposition:

    def __init__(self, domain, minimumSize):
        self.domain = domain
        self.minimumSize = minimumSize
        self.root = [Rectangle(0.0, 0.0, domain.width, domain.height), 'unknown', []]

    def Draw(self, ax, node = None):
            if ( node == None ):
                node = self.root
            r = plt.Rectangle((node[0].x, node[0].y), node[0].width, node[0].height, fill=False, facecolor=None, alpha=0.5)
            if ( node[1] == 'mixed' ):
                color = '#5080ff'
                if ( node[2] == [] ):
                    r.set_fill(True)
                    r.set_facecolor(color)
            elif ( node[1] == 'free' ):
                color = '#ffffff'
                r.set_fill(True)
                r.set_facecolor(color)
            elif ( node[1] == 'obstacle'):
                color = '#5050ff'
                r.set_fill(True)
                r.set_facecolor(color)
            else:
                print("Error: don't know how to draw cell of type", node[1])
            #print('Draw node', node)
            ax.add_patch(r)
            #ax.scatter(node[0].center_x, node[0].center_y, color='k', s=1, alpha=1.0)
            for c in node[2]:
                self.Draw(ax, c)

    def CountCells(self, node = None ):
        if ( node is None ):
            node = self.root
        sum = 0
        if ( node[2] != [] ):
            sum = 0
            for c in node[2]:
                sum = sum + self.CountCells(c)
        else:
            sum = 1
        return sum

class QuadTreeDecomposition(CellDecomposition):
    def __init__(self, domain, minimumSize):
        super().__init__(domain, minimumSize)
        self.root = self.Decompose(self.root)

    def Decompose(self, node):
        cell = 'free'
        r = node[0]
        rx = r.x
        ry = r.y
        rwidth = r.width
        rheight = r.height

        for o in self.domain.obstacles:
            if ( o.CalculateOverlap(r) >= rwidth * rheight ):
                cell = 'obstacle'
                break
            elif ( o.CalculateOverlap(r) > 0.0 ):
                cell = 'mixed'
                break
        if ( cell == 'mixed'):
            if (rwidth / 2.0 > self.minimumSize) and (rheight / 2.0 > self.minimumSize):
                childt1 = [Rectangle(rx, ry, rwidth/2.0, rheight/2.0), 'unknown', [] ]
                qchild1 = self.Decompose( childt1 )
                childt2 = [Rectangle(rx + rwidth/2.0, ry, rwidth/2.0, rheight/2.0), 'unknown', [] ]
                qchild2 = self.Decompose( childt2 )
                childt3 = [Rectangle(rx, ry + rheight/2.0, rwidth/2.0, rheight/2.0), 'unknown', [] ]
                qchild3 = self.Decompose( childt3 )
                childt4 = [Rectangle(rx + rwidth/2.0, ry + rheight/2.0, rwidth/2.0, rheight/2.0), 'unknown', [] ]
                qchild4 = self.Decompose( childt4 )
                children = [ qchild1, qchild2, qchild3, qchild4 ]
                node[2] = children
            else:
                cell = 'obstacle'
        node[1] = cell
        return node


class BinarySpacePartitioning(CellDecomposition):
    def __init__(self, domain, minimumSize ):
        super().__init__(domain, minimumSize)
        self.root = self.Decompose(self.root)

    def Entropy(self, p):
        e = 0.0
        if ( ( p > 0 ) and ( p < 1.0 ) ):
            e = -p * math.log(p,2) - (1-p) * math.log(1-p,2)
        return e

    def CalcEntropy(self, rect):
        area = rect.width * rect.height
        a = 0.0
        for o in self.domain.obstacles:
            a = a + rect.CalculateOverlap(o)
        p = a / area
        return self.Entropy(p)

    def Decompose(self, node):
        cell = 'free'
        r = node[0]
        rx = r.x
        ry = r.y
        rwidth = r.width
        rheight = r.height
        area = rwidth * rheight

        for o in self.domain.obstacles:
            if ( o.CalculateOverlap(r) >= rwidth * rheight ):
                cell = 'obstacle'
                break
            elif ( o.CalculateOverlap(r) > 0.0 ):
                cell = 'mixed'
                break

        if ( cell == 'mixed'):
            entropy = self.CalcEntropy(r)
            igH = 0.0
            hSplitTop = None
            hSplitBottom = None
            vSplitLeft = None
            vSplitRight = None
            if ( r.height / 2.0 > self.minimumSize):
                hSplitTop = Rectangle(rx, ry + rheight/2.0, rwidth, rheight/2.0)
                entHSplitTop = self.CalcEntropy(hSplitTop)
                hSplitBottom = Rectangle(rx, ry, rwidth, rheight/2.0)
                entHSplitBottom = self.CalcEntropy( hSplitBottom )

                igH = entropy - ( r.width * r.height / 2.0 ) / area * entHSplitTop \
                      - ( r.width * r.height / 2.0 ) / area * entHSplitBottom
            igV = 0.0
            if ( r.width / 2.0 > self.minimumSize ):
                vSplitLeft = Rectangle(rx, ry, rwidth/2.0, rheight )
                entVSplitLeft = self.CalcEntropy( vSplitLeft )
                vSplitRight = Rectangle( rx + rwidth/2.0, ry, rwidth/2.0, rheight)
                entVSplitRight = self.CalcEntropy( vSplitRight)
                igV = entropy - ( r.width/2.0 * r.height ) / area * entVSplitLeft \
                      - ( r.width/2.0 * r.height ) / area * entVSplitRight
            children = []
            if ( igH > igV ):
                if ( igH > 0.0 ):
                    if ( hSplitTop is not None ) and ( hSplitBottom is not None ):
                        childTop = [ hSplitTop, 'unknown', [] ]
                        childBottom = [hSplitBottom, 'unknown', [] ]
                        children = [ childTop, childBottom]
            else:
                if ( igV > 0.0 ):
                    if ( vSplitLeft is not None ) and ( vSplitRight is not None ):
                        childLeft = [vSplitLeft, 'unknown', [] ]
                        childRight = [ vSplitRight, 'unknown', [] ]
                        children = [ childLeft, childRight ]
            for c in children:
                self.Decompose(c)
            node[2] = children
        node[1] = cell
        return node

def get_leaf_nodes(root):
    children = root[2]
    if root[1] == 'free':
        return [root[0]]
    else:
        return sum([get_leaf_nodes(child) for child in children], [])




def A_star(start, goal, ax=None):

    visited_nodes = [] # for animation

    def heuristic(node_0, node_1):
        rec_0 = node_0.rectangle
        rec_1 = node_1.rectangle

        return np.sqrt(np.sum((rec_0.center - rec_1.center) ** 2))

    def dist_between(node_0, node_1):
        rec_0 = node_0.rectangle
        rec_1 = node_1.rectangle

        return np.sqrt(np.sum((rec_0.center - rec_1.center) ** 2))

    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path

    closed_set = set()
    open_set = {start}

    came_from = dict()

    g_score = defaultdict(lambda: 1e6)
    g_score[start] = 0

    f_score = defaultdict(lambda: 1e6)
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = sorted(open_set, key=lambda node: f_score[node])[0]
        visited_nodes.append(current)

        # if ax:
        #     ax.scatter(current.rectangle.center_x, current.rectangle.center_y, color='k', s=1)
        #     plt.pause(0.001)

        if current == goal:
            return reconstruct_path(came_from, current), visited_nodes

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in current.adjacent_nodes:
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + dist_between(current, neighbor)

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)




def main( argv = None ):

    seed = random.randrange(4190)
    random.Random(seed)
    np.random.seed(seed)
    print(seed)

    if ( argv == None ):
        argv = sys.argv[1:]

    width = 10.0
    height = 10.0

    pp = PathPlanningProblem( width, height, 15, 3.0, 3.0)
    #pp.obstacles = [ Obstacle(0.0, 0.0, pp.width, pp.height / 2.2, '#555555' ) ]
    initial, goals = pp.CreateProblemInstance()

    #fig = plt.figure()
    fig, ax = plt.subplots(figsize=(5,5))
    #ax = fig.add_subplot(1,2,1, aspect='equal')
    ax.set_xlim(0.0, width)
    ax.set_ylim(0.0, height)

    for o in pp.obstacles:
        ax.add_patch(copy.copy(o.patch) )
    ip = plt.Rectangle((initial[0],initial[1]), 0.1, 0.1, facecolor='#ff0000')
    ax.add_patch(ip)

    for g in goals:
        g = plt.Rectangle((g[0],g[1]), 0.1, 0.1, facecolor='#00ff00')
        ax.add_patch(g)

    qtd = QuadTreeDecomposition(pp, 0.1) # 0.2
    qtd.Draw(ax)
    n = qtd.CountCells()
    ax.set_title('Quadtree Decomposition\n{0} cells'.format(n))

    result = get_leaf_nodes(qtd.root)
    #plt.pause(0.1)
    search_nodes = []
    initial_node, goal_node = None, None
    for rec in result:
        #ax.scatter(rec.center_x, rec.center_y, color='k', s=1, alpha=1.0)
        node = SearchNode(rec)
        search_nodes.append(node)

        if rec.ContainsPoint(*goals[0]):
            ax.scatter(rec.center_x, rec.center_y, color='#00ff00', s=1)
            goal_node = node

        if rec.ContainsPoint(*initial):
            ax.scatter(rec.center_x, rec.center_y, color='#ff0000', s=1)
            initial_node = node

        #plt.pause(0.001)

    n = len(search_nodes)
    for i in range(n):
        for j in range(i+1, n):
            node_i = search_nodes[i]
            node_j = search_nodes[j]

            if node_i.rectangle.SharesEdge(node_j.rectangle):
                node_i.add_adjacent(node_j)
                node_j.add_adjacent(node_i)


    if initial_node and goal_node:
        print('solving...', end=' ')
        path, visited = A_star(initial_node, goal_node, ax=None)
        print('done!')
        if result is None:
            print('no solution!')
    else:
        print('bad nodes')
        print(initial_node)
        print(goal_node)
        exit(1)



    # def update(i):
    #     #for node in visited:
    #     rec = visited[i].rectangle
    #     ax.scatter(rec.center_x, rec.center_y, color='k', s=1, alpha=1.0)
    #     # plt.pause(0.001)
    #     return ax
    #
    # print('animating...', end=' ')
    # gif = FuncAnimation(fig, update, frames=range(len(visited)), interval=10)
    # print('done!')
    # print('saving...', end=' ')
    # gif.save('test.gif', dpi=120, writer='imagemagick')
    # print('done!')
    # #plt.show()

    for node in visited:
        rec = node.rectangle
        ax.scatter(rec.center_x, rec.center_y, color='k', s=1, alpha=1.0)
        plt.pause(0.001)

    path_coords = np.array([node.rectangle.center for node in path])
    ax.plot(*path_coords.T, 'r-')

    plt.show()


if ( __name__ == '__main__' ):
    main()


