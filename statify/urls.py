from django.urls import path

from . import views

app_name = 'statify'
urlpatterns = [
    path('', views.index, name='index'),
    path('spotifyauth', views.spotifyauth, name='spotifyauth'),
    path('callback', views.callback, name='callback'),
    path('profile', views.profile, name='profile')
]
