from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('create/<int:game_id>/', views.create_character, name='create_character'),
    path('create_game/', views.create_game, name="create_game"),
    path('list/', views.list, name="list"),
    path('detail/<int:game_id>',views.detail, name="detail"),
    path('play/<int:game_id>', views.play, name="play"),
    path('send_message/', views.send_message, name="send"),
]