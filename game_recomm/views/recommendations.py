from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from game_recomm.models.game_recomm import Game, GameRating
from game_recomm.serializers import GameRecommendationSerializer, RatingSerializer
from rest_framework.decorators import permission_classes
from game_recomm.permissions import IsAdminOrReadOnly, IsNonAdminNonStaffUser
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from django.db.models import Q


@api_view(['GET'])
@permission_classes([AllowAny])
def get_game_list(request):
    game = Game.objects.all()
    serializer = GameRecommendationSerializer(game, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_games_by_categories(request):
    categories = request.data.get('categories', [])
    if not isinstance(categories, list) or not categories:
        return Response({"detail": "Please provide a list of categories."}, status=400)

    # Build a dynamic Q object for any matching category
    query = Q()
    for category in categories:
        query |= Q(category__contains=category)

    # Fetch games based on the provided categories using the dynamic Q object
    games = Game.objects.filter(query)
    serializer = GameRecommendationSerializer(games, many=True)
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


class RateGameView(APIView):
    permission_classes = [IsNonAdminNonStaffUser]

    def get_game(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=404)

    def post(self, request, pk):
        game = self.get_game(pk)
        if not game:
            return Response({"detail": "Game not found."}, status=404)

        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            rating = serializer.validated_data['game_rating']
            if GameRating.objects.filter(user=request.user, game=game):
                # If the user already left a rating, they can only use PUT to update it
                return Response(
                    {"detail": "You have already rated this game. Use PUT to update or DELETE to remove your rating."},
                    status=400)

            # Create or update the rating for the current user and game
            game_rating, created = GameRating.objects.update_or_create(
                user=request.user,
                game=game,
                defaults={'game_rating': rating}
            )

            # Update the total_score and num_ratings
            game.score += rating
            game.num_ratings += 1
            game.average_score = game.score / game.num_ratings

            # Save the changes
            game.save()

            # If the rating is created, return 201 Created, otherwise return 200 OK
            status_code = 201 if created else 200

            # Return a success response
            return Response({"detail": "Rating added successfully."}, status=status_code)
        else:
            # Return a bad request response with the validation errors
            return Response(serializer.errors, status=400)

    def put(self, request, pk):
        game = self.get_game(pk)
        if not game:
            return Response({"detail": "Game not found."}, status=404)
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            rating = serializer.validated_data['game_rating']
            if not GameRating.objects.filter(user=request.user, game=game):
                return Response('You first need to leave a rating to update it', status=403)
            try:
                game_rating = GameRating.objects.get(user=request.user, game=game)
                previous_rating = game_rating.game_rating
                # Update the total_score by subtracting the previous rating
                game.score -= previous_rating
            except GameRating.DoesNotExist:
                game_rating = None

            # Create or update the rating for the current user and game
            game_rating, created = GameRating.objects.update_or_create(
                user=request.user,
                game=game,
                defaults={'game_rating': rating}
            )

            # Update the total_score and num_ratings
            game.score += rating
            game.average_score = game.score / game.num_ratings
            # Save the changes
            game.save()

            # If the rating is created, return 201 Created, otherwise return 200 OK
            status_code = 201 if created else 200

            # Return a success response
            return Response({"detail": "Rating added successfully."}, status=status_code)
        else:
            # Return a bad request response with the validation errors
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        game = self.get_game(pk)
        if not game:
            return Response({"detail": "Game not found."}, status=404)

        try:
            game_rating = GameRating.objects.get(user=request.user, game=game)
            rating_value = game_rating.game_rating

            # Update the score and num_ratings
            game.score -= rating_value
            game.num_ratings -= 1

            # Calculate the average_score
            if game.num_ratings > 0:
                game.average_score = game.score / game.num_ratings
            else:
                game.average_score = 0.0  # Set average_score to 0 if there are no ratings.

            # Save the changes
            game.save()

            game_rating.delete()
            return Response({"detail": "Rating deleted successfully."}, status=204)
        except GameRating.DoesNotExist:
            return Response({"detail": "Rating not found."}, status=404)

