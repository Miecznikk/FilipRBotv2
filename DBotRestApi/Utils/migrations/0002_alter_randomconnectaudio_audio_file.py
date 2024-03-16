# Generated by Django 4.2.6 on 2024-03-13 19:30

import Utils.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utils', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='randomconnectaudio',
            name='audio_file',
            field=models.FileField(upload_to='audio_files/random_connect', validators=[Utils.models.validate_mp3]),
        ),
    ]
