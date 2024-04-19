from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Role(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class GameRole(Role):
    game_assigned = models.CharField(max_length=50, null=False)
    game_detection_string = models.CharField(max_length=255, null=False)


class Member(models.Model):
    name = models.CharField(max_length=50, null=False)
    points = models.IntegerField(default=0, null=False)
    minutes_spent = models.IntegerField(default=0, null=False)
    configurator = models.BooleanField(default=False)
    nicknames = models.CharField(max_length=250, null=False, default="")

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your models here.
