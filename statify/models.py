from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class SpotifyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spotify_username = models.CharField(max_length=100)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        SpotifyUser.objects.create(user=instance)

    instance.spotifyuser.save()
