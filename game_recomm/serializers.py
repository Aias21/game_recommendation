from rest_framework import serializers
from .models.game_recomm import Game, GameRating, CATEGORIES
from rest_framework.validators import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import date

class UniqueTitleValidator:
    def __call__(self, value):
        if Game.objects.filter(title=value).exists():
            raise ValidationError(f'Game with title "{value}" already exists!')


class DateValidator:
    def __call__(self, value):
        if value > date.today():
            raise ValidationError(f'Date must be smaller than {date.today()}')


class RatingSerializer(serializers.ModelSerializer):
    game_rating = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    class Meta:
        model = GameRating
        fields = ('game_rating',)


# class GameCategorySerializer(serializers.ModelSerializer):
#     category = serializers.MultipleChoiceField(choices=CATEGORIES)
#     class Meta:
#         model = Game
#         fields = ('title', 'description', 'release_date', 'category', 'game_rating', 'num_ratings', 'score', 'average_score')


class GameRecommendationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    category = serializers.MultipleChoiceField(choices=CATEGORIES)
    game_rating = RatingSerializer(many=True, read_only=True)
    release_date = serializers.DateField(validators=[DateValidator()])

    class Meta:
        model = Game
        fields = ('title', 'description', 'release_date', 'category', 'game_rating', 'num_ratings', 'score', 'average_score')

    def to_internal_value(self, data):
        categories = data.get('category', [])
        if not isinstance(categories, list):
            categories = [categories]
        data['category'] = categories
        return super().to_internal_value(data)


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    email = serializers.EmailField(max_length=200, required=True)


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)