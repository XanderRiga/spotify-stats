from django.urls import path

from . import views

app_name = 'statify'
urlpatterns = [
    path('', views.signup, name='signup'),
    path('spotifyauth', views.spotifyauth, name='spotifyauth'),
    path('callback', views.callback, name='callback'),
    path('profile', views.profile, name='profile'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('login_user', views.login_user, name='login_user')
]
