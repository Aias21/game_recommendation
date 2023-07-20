from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

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

class Game(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    release_date = models.DateField()
    # categories = models.ManyToManyField(GameCategory)
    category = MultiSelectField(max_length=20, choices=CATEGORIES,
                            default=DEFAULT_CATEGORY, null=True, blank=True)
    score = models.IntegerField(default=0)  # score received from ratings
    num_ratings = models.IntegerField(default=0)  # Number of ratings received
    average_score = models.FloatField(default=0)

    def __str__(self):
        return self.title


class GameRating(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings', default=None)
    game_rating = models.IntegerField(default=None, validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        unique_together = ('game', 'user')