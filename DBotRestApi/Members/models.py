from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Role(models.Model):
    name = models.CharField(max_length=50, null=False)


class Member(models.Model):
    name = models.CharField(max_length=50, null=False)
    points = models.IntegerField(default=0, null=False)
    minutes_spent = models.IntegerField(default=0, null=False)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your models here.
