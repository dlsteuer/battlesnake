"""A graph used for A* pathfinding"""

class Graph(object):
    """Class representing a Graph"""
    all_nodes = []
    inaccessible_nodes = []

    def __init__(self):
        return

    def init(self, width, height):
        """Initializes the graph"""
        for x_coord in range(width):
            for y_coord in range(height):
                self.all_nodes.append((x_coord, y_coord))

    def update(self, blackboard):
        """Updates graph based on blackboard data"""
        self.inaccessible_nodes = []
        snakes = blackboard['snakes']

        for snake in snakes:
            coords = snake['coords']

            for coord in coords:
                x_coord = coord[0]
                y_coord = coord[1]
                self.inaccessible_nodes.append((x_coord, y_coord))


    def neighbors(self, node):
        """Returns a list of neighbors of the parameter node"""
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        results = []
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if neighbor in self.all_nodes and neighbor not in self.inaccessible_nodes:
                results.append(neighbor)
        return results

    def cost(self, node_1, node_2):
        """Returns cost of navigating between two nodes"""
        (x_coord_1, y_coord_1) = node_1
        (x_coord_2, y_coord_2) = node_2
        return abs(x_coord_1 - x_coord_2) + abs(y_coord_1 - y_coord_2)
