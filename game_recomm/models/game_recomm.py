from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

CATEGORIES = (
    ('Action', 'Action'),
    ('Adventure', 'Adventure'),
    ('Indie', 'Indie'),
    ('Platformer', 'Platformer'),
    ('RPG', 'RPG'),
    ('Strategy', 'Strategy'),
    ('Shooter', 'Shooter'),
    ('Sports', 'Sports'),
    ('Racing', 'Racing'),
)

DEFAULT_CATEGORY = None


class GameCategory(models.Model):
    name = models.CharField(max_length=20, choices=((DEFAULT_CATEGORY, '-Select category-'),) + CATEGORIES, default=DEFAULT_CATEGORY)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    release_date = models.DateField()
    categories = models.ManyToManyField(GameCategory)

class GameRating(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_rating')
    game_rating = models.IntegerField(default=None, validators=[MinValueValidator(1), MaxValueValidator(10)])