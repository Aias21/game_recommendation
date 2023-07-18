from django.urls import path
from .views.recommendations import get_game_list
from.views.user import RegisterUser, LoginUser


app_name = 'game_recomm'
urlpatterns = [
    path('', get_game_list, name='recommendations-list'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='log_in'),
]