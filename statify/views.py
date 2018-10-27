from django.http import Http404, HttpResponse
import spotipy
import spotipy.util as util
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.shortcuts import render, redirect


SPOTIPY_CLIENT_ID = 'ff706cadbcd2445782b2c3719bace226'
SPOTIPY_CLIENT_SECRET = '538dc4b9fd7e4da48df760c4a99f2e1d'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/statify/callback'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'


def signup(request):
    if request.user.is_authenticated:
        return redirect('statify:profile')

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
    return render(request, 'statify/signup.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('statify:signup')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('statify:profile')

    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('statify:profile')
        else:
            return render(request, 'statify/loginform.html')
    except:
        return render(request, 'statify/loginform.html')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('statify:signup')
    user = request.user
    return render(request, 'statify/profile.html', {'user': user})


def spotifyauth(request):
    """This function checks for a cached token, and if there isn't one, then it asks the user to sign in"""
    username = request.user.spotifyuser.spotify_username
    auth_token = util.get_cached_token(username, scope=SCOPE, client_id=SPOTIPY_CLIENT_ID,
                                       client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

    if auth_token:
        return callback(request, auth_token=auth_token['access_token'], refresh_token=auth_token['refresh_token'])
    else:
        auth_url = util.prompt_for_user_token(username, scope=SCOPE, client_id=SPOTIPY_CLIENT_ID,
                                              client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)
        return redirect(auth_url)


def callback(request, auth_token=None, refresh_token=None):
    """Is either called with a cached token, or is received as a callback from spotify with the credentials"""
    if auth_token:
        pass
    else:
        auth_token = request.GET['code']

    # TODO save auth token and refresh to user object and redirect to new page to get API data

    return statshome(request, auth_token)


def statshome(request, auth_token=None):
    """Shows basic stats for the user"""
    if not auth_token:
        # TODO need to get token saved from user or refresh if necessary for faster loading
        # TODO so we don't have to go through spotifyauth every time
        pass

    sp = spotipy.Spotify(auth=auth_token)
    sp.trace = False
    results = sp.current_user()

    imageurl = results['images'][0]['url']
    display_name = results['display_name']
    spotifyname = results['id']
    country = results['country']
    accounturl = results['external_urls']['spotify']
    product = results['product']

    return render(request, 'statify/statshome.html', {
        'imageurl': imageurl,
        'spotifyname': spotifyname,
        'country': country,
        'accounturl': accounturl,
        'product': product,
        'display_name': display_name
    })
