from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.game_recomm import Game, GameRating
from ..serializers import GameRecommendationSerializer
from rest_framework.decorators import permission_classes
from ..permissions import IsAdminOrReadOnly, IsNonAdminNonStaffUser
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import AnonymousUser


@api_view(['GET'])
@permission_classes([AllowAny])
def get_game_list(request):
    game = Game.objects.all()
    serializer = GameRecommendationSerializer(game, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
@permission_classes([IsAdminOrReadOnly])
def post_game_recommendation(request):
    serializer = GameRecommendationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def recommendation_detail(request, pk):
    try:
        recommendation = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=400)
    if request.method == 'GET':
        serializer = GameRecommendationSerializer(recommendation)
        return Response(serializer.data, status=200)
    elif request.method == "PUT":
        serializer = GameRecommendationSerializer(recommendation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        recommendation.delete()
        return Response(status=204)


@api_view(['POST', 'DELETE'])
@permission_classes([IsNonAdminNonStaffUser])
def post_rate_game(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response({"detail": "Game not found."}, status=404)
    if request.method == 'POST':
        if isinstance(request.user, AnonymousUser):
            return Response({"detail": "You must be logged in to rate a game."},
                            status=401)
        # Handling the POST request for rating the game, similar to previous implementation
        rating_value = request.data.get('game_rating')
        if rating_value is not None:
            # Assuming you have a separate model for game ratings
            # Create or update the rating for the current user and game
            game_rating, created = GameRating.objects.update_or_create(
                user=request.user,
                game=game,
                defaults={'game_rating': rating_value}
            )

            # If the rating is created, return 201 Created, otherwise return 200 OK
            status_code = 201 if created else 200

            # Return a success response
            return Response({"detail": "Rating added successfully."}, status=status_code)

        # If the rating value is not provided, return a bad request response
        return Response({"detail": "Rating value is required."}, status=400)

    elif request.method == 'DELETE':
        # Handling the DELETE request for deleting the user's rating for the game
        try:
            game_rating = GameRating.objects.get(user=request.user, game=game)
            game_rating.delete()
            return Response({"detail": "Rating deleted successfully."}, status=204)
        except GameRating.DoesNotExist:
            return Response({"detail": "Rating not found."}, status=404)

    # If the request method is not POST or DELETE, return method not allowed response
    return Response({"detail": "Method not allowed."}, status=405)
