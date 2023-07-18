from django.contrib import admin
from .models.game_recomm import Game, GameRating, GameCategory

admin.site.register(Game)
admin.site.register(GameRating)
admin.site.register(GameCategory)


