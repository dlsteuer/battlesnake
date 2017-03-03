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
        'snake': {},
        'snake_len': -1,
        'snake_head_coord': (-1, -1),
        'snake_tail_coord': (-1, -1),
        'target_coord': (-1, -1),
        'path': {},
        'snakes': [],
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

        path = self.BLACKBOARD['path']

        # If no path to food exists, try finding a path to our tail
        if len(path) == 0:
            coord = self.BLACKBOARD['snake_tail_coord']

            self.BLACKBOARD['target_coord'] = (coord[0], coord[1])
            self.__find_path()

        path = self.BLACKBOARD['path']

        if len(path) == 0:
            own_cost = self.GRAPH.cost(
                self.BLACKBOARD['snake_head_coord'],
                self.BLACKBOARD['snake_tail_coord']
            )
            ideal_cost = -1
            ideal_coord = (0, 0)

            for neighbor in self.GRAPH.neighbors(self.BLACKBOARD['path']):
                cost = self.GRAPH.cost(neighbor, self.BLACKBOARD['snake_tail_coord'])

                if cost <= own_cost and cost > ideal_cost:
                    ideal_cost = cost
                    ideal_coord = neighbor

            next_coord = ideal_coord
        else:
            next_coord = self.BLACKBOARD['path'][0]

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
        self.BLACKBOARD['target_coord'] = (
            data['food'][0][0],
            data['food'][0][1]
        )
        self.__update_self(data['you'], data['snakes'])
        # Update graph
        self.GRAPH.update(self.BLACKBOARD)
        self.__find_path()
        return

    def __find_path(self):
        """Updates the A* pathing logic"""
        # Obtain path mapping based on graph and start/end points
        came_from = a_star_search(
            self.GRAPH,
            self.BLACKBOARD['snake_head_coord'],
            self.BLACKBOARD['target_coord']
        )

        # Build path array based on path mapping
        path = []
        node = self.BLACKBOARD['target_coord']
        while node != self.BLACKBOARD['snake_head_coord']:
            # If node is not in mapping, no path exists
            if node in came_from:
                path.append(node)
                node = came_from[node]
            else:
                # Set path to empty if no path exists and exit
                path = []
                break
        path.reverse()

        self.BLACKBOARD['path'] = path

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

