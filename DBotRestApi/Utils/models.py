from django.core.exceptions import ValidationError
from django.db import models


def validate_mp3(value):
    if not value.name.endswith('.mp3'):
        raise ValidationError("Only .mp3 files allowed")


class RandomConnectAudio(models.Model):
    name = models.CharField(max_length=50)
    audio_file = models.FileField(upload_to='audio_files/random_connect', validators=[validate_mp3])

    def __str__(self):
        return self.name

# Create your models here.
