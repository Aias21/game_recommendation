from django.urls import path
from .views.recommendations import get_game_list, recommendation_detail, post_game_recommendation, post_rate_game
from.views.user import RegisterUser, LoginUser


app_name = 'game_recomm'
urlpatterns = [
    path('', get_game_list, name='recommendations-list'),
    path('create/', post_game_recommendation, name='create-recommendation'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='log_in'),
    path('detail/<int:pk>/', recommendation_detail, name='detail'),
    path('rate/<int:pk>/', post_rate_game, name='rate'),
]