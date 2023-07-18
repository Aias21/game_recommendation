from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.game_recomm import Game, GameRating
from ..serializers import GameRecommendationSerializer


@api_view(['GET'])
def get_game_list(request):
    game = Game.objects.all()
    serializer = GameRecommendationSerializer(game, many=True)
    return Response(serializer.data, status=200)