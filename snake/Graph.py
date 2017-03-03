"""A graph used for A* pathfinding"""

class Graph(object):
    """Class representing a Graph"""
    all_nodes = []
    inaccessible_nodes = []

    def __init__(self):
        return

    def init(self, width, height):
        """Initializes the graph"""
        for y_coord in range(height):
            for x_coord in range(width):
                self.all_nodes.append((x_coord, y_coord))

    def update(self, blackboard):
        """Updates graph based on blackboard data"""
        self.inaccessible_nodes = []

        for snake in blackboard['snakes']:
            for coord in snake['coords']:
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

    def cost(self, start_node, end_node):
        """Returns cost of navigating between two nodes"""
        (x_coord_1, y_coord_1) = start_node
        (x_coord_2, y_coord_2) = end_node
        return abs(x_coord_1 - x_coord_2) + abs(y_coord_1 - y_coord_2)
