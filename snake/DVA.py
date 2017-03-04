"""Represents the snake AI with personality D.Va"""
import random
from .Graph import Graph
from .a_star import a_star_search

class DVA(object):
    """Represents the Battlesnake D.Va"""

    # In case server is started after game has begun
    INIT = False

    NAME = 'D.Va'
    IMAGE_URL = 'static/d_va.png'
    COLOR = '#EE4BB5'
    TAUNTS = {
        'set_up': {
            'dva_online': 'D.Va online.',
            'into_the_fight': 'I can\'t wait to get into the fight!',
            'new_high_score': 'Let\'s shoot for a new high score!',
            'gameface_on': 'Alright. Gameface: On.',
            'keep_up_with_me': 'Think you can keep up with me?',
            'lead_the_way': 'MEKA leads the way!',
            'ready_player_one': 'Ready, player 1.',
        }
    }

    # AI Blackboard
    BLACKBOARD = {
        'snake': None,
        'snake_len': None,
        'snake_head_coord': None,
        'snake_tail_coord': None,
        'nearest_snake': None,
        'nearest_food': None,
        'path': None,
        'food': None,
        'snakes': None,
    }

    GRAPH = Graph()

    def __init__(self):
        return

    def get_name(self):
        """Return snake name"""
        return self.NAME

    def get_image_url(self):
        """Return snake image"""
        return self.IMAGE_URL

    def get_color(self):
        """Returns snake color"""
        return self.COLOR

    def get_taunt(self, category, key):
        """Return taunt based on category and key parameters"""
        return self.TAUNTS[category].get(key)

    def get_random_taunt(self, category):
        """Return random taunt based on category parameter"""
        random_key = random.choice(list(self.TAUNTS[category]))

        return self.TAUNTS[category].get(random_key)

    def get_move(self):
        """Returns the next moves relative direction"""
        snake_head = self.BLACKBOARD['snake_head_coord']
        snake_tail = self.BLACKBOARD['snake_tail_coord']
        nearest_food = self.BLACKBOARD['nearest_food']
        nearest_snake = self.BLACKBOARD['nearest_snake']

        (nearest_food_cost, nearest_food_coord) = nearest_food

        if nearest_snake is not None:
            (nearest_snake_cost, nearest_snake_object) = nearest_snake
            nearest_snake_head = (
                nearest_snake_object['coords'][0][0],
                nearest_snake_object['coords'][0][1]
            )

            nearest_food_nearest_snake_cost = self.GRAPH.cost(
                nearest_food_coord,
                nearest_snake_head
            )

        current_path_to_tail = self.__find_path(
            snake_head,
            snake_tail
        )

        if nearest_snake is None or nearest_food_cost <= nearest_food_nearest_snake_cost:
            path = self.__find_path(
                self.BLACKBOARD['snake_head_coord'],
                nearest_food_coord
            )
        else:
            path = current_path_to_tail

        # If no path to food exists, try finding a path to our tail
        if len(path) == 0:
            path = current_path_to_tail

        if len(path) == 0:
            coord_1 = self.BLACKBOARD['snake_head_coord']
            coord_2 = self.GRAPH.farthest_node(self.BLACKBOARD['snake_head_coord'])
            path = self.__find_path(coord_1, coord_2)

        next_coord = path[0]
        future_path_to_tail = self.__find_path(next_coord, self.BLACKBOARD['snake_tail_coord'])

        if len(future_path_to_tail) == 0 and len(current_path_to_tail) > 0:
            next_coord = current_path_to_tail[0]

        diff = (
            next_coord[0] - self.BLACKBOARD['snake_head_coord'][0],
            next_coord[1] - self.BLACKBOARD['snake_head_coord'][1]
        )

        if diff == (0, 1):
            return 'down'
        elif diff == (0, -1):
            return 'up'
        elif diff == (1, 0):
            return 'right'
        else:
            return 'left'

    def init(self, data):
        """Initializes object based on Battlesnake game data"""
        self.GRAPH.init(data['width'], data['height'])
        return

    def update(self, data):
        """Updates object based on Battlesnake turn data"""
        # Check if we're initialized, if not, init
        if not self.INIT:
            self.init(data)

        self.BLACKBOARD['snakes'] = data['snakes']
        self.BLACKBOARD['food'] = data['food']
        self.__update_self(data['you'], data['snakes'])
        # Update graph
        self.GRAPH.update(self.BLACKBOARD)

        nearest_snake = self.__find_nearest_snake()
        nearest_food = self.__find_nearest_food()

        if nearest_snake is not None:
            self.BLACKBOARD['nearest_snake'] = nearest_snake

        if nearest_food is not None:
            self.BLACKBOARD['nearest_food'] = nearest_food

        return

    def __update_self(self, snake_id, snakes):
        """Updates snake based on Battlesnake turn data"""
        for snake in snakes:
            if snake_id == snake['id']:
                snake_len = len(snake['coords'])
                self.BLACKBOARD['snake'] = snake
                self.BLACKBOARD['snake_len'] = snake_len
                self.BLACKBOARD['snake_head_coord'] = (
                    snake['coords'][0][0],
                    snake['coords'][0][1]
                )
                self.BLACKBOARD['snake_tail_coord'] = (
                    snake['coords'][snake_len - 1][0],
                    snake['coords'][snake_len - 1][1]
                )
        return

    def __find_nearest_snake(self):
        coord_1 = self.BLACKBOARD['snake_head_coord']
        snakes = self.BLACKBOARD['snakes']
        lowest_cost = -1
        lowest_cost_snake = None

        for snake in snakes:
            coord_2 = snake['coords'][0]
            cost = self.GRAPH.cost(coord_1, coord_2)

            if lowest_cost == -1 or cost < lowest_cost:
                lowest_cost_snake = snake
                lowest_cost = cost

        return (lowest_cost, lowest_cost_snake)

    def __find_nearest_food(self):
        food = self.BLACKBOARD['food']
        coord_1 = self.BLACKBOARD['snake_head_coord']
        lowest_cost_coord = None
        lowest_cost = -1

        for food_coord in food:
            coord_2 = (food_coord[0], food_coord[1])
            cost = self.GRAPH.cost(
                coord_1,
                coord_2
            )
            if lowest_cost == -1 or lowest_cost > cost:
                lowest_cost_coord = coord_2
                lowest_cost = cost

        return (lowest_cost, lowest_cost_coord)

    def __find_path(self, node_1, node_2):
        """Updates the A* pathing logic"""
        # Obtain path mapping based on graph and start/end points
        came_from = a_star_search(
            self.GRAPH,
            node_1,
            node_2
        )

        # Build path array based on path mapping
        path = []
        node = node_2
        while node != node_1:
            # If node is not in mapping, no path exists
            if node in came_from:
                path.append(node)
                node = came_from[node]
            else:
                # Set path to empty if no path exists and exit
                path = []
                break
        path.reverse()

        return path
