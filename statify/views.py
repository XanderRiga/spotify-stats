from django.http import Http404, HttpResponse
from django.shortcuts import render

from .models import User
import spotipy
import spotipy.util as util

SPOTIPY_CLIENT_ID = 'ff706cadbcd2445782b2c3719bace226'
SPOTIPY_CLIENT_SECRET = '538dc4b9fd7e4da48df760c4a99f2e1d'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/statify/callback'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'


def index(request):
    all_users = User.objects.all()
    return render(request, 'statify/index.html', {'all_users': all_users})


def detail(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404('User does not exist')

    return render(request, 'statify/detail.html', {'user': user})


def spotifyauth(request):
    username = 'xanderdagr8'
    token = util.prompt_for_user_token(username, scope=SCOPE, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None
    return
    # return render(request, 'statify/savedtracks.html', results)


def callback(request):
    return HttpResponse('Spotify successfully logged in. You can close this window and return to your previous tab')
