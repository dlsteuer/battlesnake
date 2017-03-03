from rest_framework.decorators import api_view
from rest_framework.response import Response
from .DVA import DVA

DVA = DVA()

@api_view(['POST'])
def start(request):
    response = dict(
        color=DVA.get_color(),
        taunt=DVA.get_random_taunt('set_up'),
        head_url="%s%s" % (request.build_absolute_uri('/'), DVA.get_image_url()),
        name=DVA.get_name()
    )
    return Response(response)


@api_view(['POST'])
def move(request):
    data = request.data

    DVA.update(data)
    move = DVA.get_move()
    response = dict(
        move=move
    )
    return Response(response)
