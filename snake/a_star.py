"""A* algorithm based on http://www.redblobgames.com/pathfinding/a-star/implementation.html"""
from Queue import PriorityQueue
import time
import heapq

def heuristic(coord_1, coord_2):
    """Determines the approximate cost going from one coord to another"""
    (x_coord_1, y_coord_1) = coord_1
    (x_coord_2, y_coord_2) = coord_2
    return abs(x_coord_1 - x_coord_2) + abs(y_coord_1 - y_coord_2)

def alt_a_star_search(graph, start_node, goal_node):
    """Find the shortest path from START to FINISH."""
    heap = []

    link = {} # parent node link
    h = {} # heuristic function cache
    g = {} # shortest path to a node

    g[start_node] = 0
    h[start_node] = 0
    link[start_node] = None


    heapq.heappush(heap, (0, 0, start_node))
    # keep a count of the  number of steps, and avoid an infinite loop.
    for kk in xrange(1000000):
        f, junk, current = heapq.heappop(heap)
        print start_node, current, goal_node
        if current == goal_node:
            print "distance:", g[current], "steps:", kk
            return link

        neighbors = graph.neighbors(current)
        distance = g[current]
        for neighbor in neighbors:
            if neighbor not in g or g[neighbor] > distance + 1:
                g[neighbor] = distance + 1
                if neighbor not in h:
                    h[neighbor] = heuristic(neighbor, goal_node)
                link[neighbor] = current
                heapq.heappush(heap, (g[neighbor] + h[neighbor], -kk, neighbor))

def a_star_search(graph, start_node, goal_node):
    """Determines a good path from start to goal based on heuristic"""
    start = time.time()
    to_visit = PriorityQueue()
    to_visit.put((0, start_node))
    came_from = {}
    cost_so_far = {}
    came_from[start_node] = None
    cost_so_far[start_node] = 0

    while not to_visit.empty():
        current = to_visit.get()[1]

        if current == goal_node:
            break

        for next_node in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal_node, next_node)
                to_visit.put((priority, next_node))
                came_from[next_node] = current

    end = time.time()
    print "a_star_search(%s, %s) runtime: %.3f" % (start_node, goal_node, (end - start))

    return came_from
