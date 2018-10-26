from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect

import spotipy
import spotipy.util as util
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.shortcuts import render, redirect


SPOTIPY_CLIENT_ID = 'ff706cadbcd2445782b2c3719bace226'
SPOTIPY_CLIENT_SECRET = '538dc4b9fd7e4da48df760c4a99f2e1d'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/statify/callback'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'


def index(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.spotifyuser.spotify_username = form.cleaned_data.get('spotify_username')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('statify:profile')
    else:
        form = SignUpForm()
    return render(request, 'statify/index.html', {'form': form})


def profile(request):
    user = request.user
    return render(request, 'statify/detail.html', {'user': user})


def spotifyauth(request):
    val = URLValidator()

    username = 'xanderdagr8'
    # auth_url = util.prompt_for_user_token(username, scope=SCOPE, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

    auth_token = util.get_cached_token(username, scope=SCOPE, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

    if auth_token:
        return redirect('callback')
    # try:
    #     val(auth_url)
    #     return HttpResponseRedirect(auth_url)
    # except ValidationError:
    #     auth_token = auth_url
    #
    #     sp = spotipy.Spotify(auth=auth_token)
    #     sp.trace = False
    #     results = sp.current_user_saved_tracks()
    #     return render(request, 'statify/savedtracks.html', {'tracks': results['items']})


def callback(request):
    code = ''
    try:
        code = request.GET['code']
    except:
        pass
    return HttpResponse('code: ' + code)
