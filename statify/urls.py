from django.urls import path

from . import views

app_name = 'statify'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>', views.detail, name='detail'),
    path('spotifyauth', views.spotifyauth, name='spotifyauth'),
    path('callback', views.callback, name='callback')
]
