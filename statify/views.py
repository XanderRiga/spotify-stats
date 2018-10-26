from django.http import Http404
from django.shortcuts import render

from .models import User


def index(request):
    all_users = User.objects.all()
    return render(request, 'statify/index.html', {'all_users': all_users})


def detail(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404('User does not exist')

    return render(request, 'statify/detail.html', {'user': user})
