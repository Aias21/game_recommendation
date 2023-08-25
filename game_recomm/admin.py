from django.contrib import admin
from .models.game_recomm import Game, GameRating  # GameCategory


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'num_ratings', 'score', 'average_score', 'release_date', 'category')

    def categories_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])


class GameRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'user', 'game_rating')


admin.site.register(Game, GameAdmin)
admin.site.register(GameRating, GameRatingAdmin)




