from rest_framework.decorators import api_view
from rest_framework.response import Response
from .DVA import DVA

GAMES = []

@api_view(['POST'])
def start(request):
    """Handles a start request"""
    game_id = request.data['game_id']
    game = get_game(game_id)

    if not game:
        game = (game_id, DVA())
        GAMES.append(game)

    game_id, dva = game

    response = dict(
        color=dva.get_color(),
        taunt=dva.get_random_taunt('set_up'),
        head_url="%s%s" % (request.build_absolute_uri('/'), dva.get_image_url()),
        name=dva.get_name()
    )
    return Response(response)


@api_view(['POST'])
def move(request):
    """Handles a move request"""
    data = request.data
    game_id = request.data['game_id']
    game = get_game(game_id)

    if not game:
        game = (game_id, DVA())
        GAMES.append(game)

    game_id, dva = game

    dva.update(data)
    move = dva.get_move()
    response = dict(
        move=move,
        taunt=dva.get_random_taunt('set_up')
    )
    return Response(response)

def get_game(game_id):
    """Returns a game instance"""
    for game in GAMES:
        local_game_id, dva = game
        if game_id == local_game_id:
            return dva

    return None
