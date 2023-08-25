from django.urls import path
from game_recomm.views.recommendations import (
    get_game_list,
    recommendation_detail,
    post_game_recommendation,
    RateGameView,
    get_games_by_categories
)
from game_recomm.views.user import RegisterUser, LoginUser, get_registration



app_name = 'game_recomm'
urlpatterns = [
    path('register/', get_registration, name='register'),
    path('api/list/', get_game_list, name='api-recommendations-list'),
    path('api/in-categories/', get_games_by_categories, name='api-in-category'),
    path('api/create/', post_game_recommendation, name='api-create-recommendation'),
    path('api/register/', RegisterUser.as_view(), name='api-register'),
    path('api/login/', LoginUser.as_view(), name='api-log_in'),
    path('api/detail/<int:pk>/', recommendation_detail, name='api-detail'),
    path('api/rate/<int:pk>/', RateGameView.as_view(), name='api-rate'),
]