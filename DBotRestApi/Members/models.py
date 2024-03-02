from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, null=False)


class Member(models.Model):
    name = models.CharField(max_length=50, null=False)
    points = models.IntegerField(default=0, null=False)
    minutes_spent = models.IntegerField(default=0, null=False)

# Create your models here.
