from django.contrib import admin
from .models.game_recomm import Game, GameRating  # GameCategory
from .models.admin_panel import GameAdmin, GameRatingAdmin  # GameCategoryAdmin


admin.site.register(Game, GameAdmin)
admin.site.register(GameRating, GameRatingAdmin)
# admin.site.register(GameCategory, GameCategoryAdmin)



