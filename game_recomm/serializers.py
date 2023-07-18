from rest_framework import serializers
from .models.game_recomm import Game, GameRating


class GameRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('title', 'description', 'release_date', 'category')


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    email = serializers.EmailField(max_length=200, required=True)


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)