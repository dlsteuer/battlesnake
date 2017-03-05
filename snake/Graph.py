"""A graph used for A* pathfinding"""

class Graph(object):
    """Class representing a Graph"""
    all_nodes = []
    inaccessible_nodes = []
    width = -1
    height = -1

    def __init__(self):
        return

    def init(self, width, height):
        """Initializes the graph"""
        self.width = width
        self.height = height
        for x_coord in range(width):
            for y_coord in range(height):
                self.all_nodes.append((x_coord, y_coord))

    def update(self, blackboard):
        """Updates graph based on blackboard data"""
        self.inaccessible_nodes = []
        snakes = blackboard['snakes']

        for snake in snakes:
            coords = snake['coords']

            for index in range(len(coords)) - 1:
                coord = coords[index]
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

    def farthest_node(self, node_1):
        """Get a farthest point given a node"""
        nodes = self.__flood_fill(node_1)
        highest_cost_node = (-1, -1)
        highest_cost = -1

        for node_2 in nodes:
            cost = self.cost(node_1, node_2)
            if cost > highest_cost:
                highest_cost_node = node_2
                highest_cost = cost

        return highest_cost_node

    def __flood_fill(self, node):
        """Flood fills based on current node"""
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        results = [node]
        nodes = [node]
        while len(nodes) > 0:
            eval_node = nodes.pop()
            for direction in directions:
                neighbor = (eval_node[0] + direction[0], eval_node[1] + direction[1])
                if (
                        neighbor not in results
                        and self.is_node_in_bounds(neighbor)
                        and neighbor not in self.inaccessible_nodes
                ):
                    results.append(neighbor)
                    nodes.append(neighbor)
        return results

    def is_node_in_bounds(self, node):
        """Make sure node is in bounds"""
        (x_coord, y_coord) = node

        if x_coord < 0 or x_coord >= self.width:
            return False
        elif y_coord < 0 or y_coord >= self.height:
            return False
        else:
            return True
