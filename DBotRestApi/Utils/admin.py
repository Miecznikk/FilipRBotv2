from django.contrib import admin
from .models import RandomConnectAudio


@admin.register(RandomConnectAudio)
class RandomConnectAudioAdmin(admin.ModelAdmin):
    list_display = ['name']
# Register your models here.
