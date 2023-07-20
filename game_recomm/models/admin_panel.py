from django.contrib import admin


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'num_ratings', 'score', 'average_score', 'release_date', 'category')

    def categories_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

# class GameCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)

class GameRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'user', 'game_rating')