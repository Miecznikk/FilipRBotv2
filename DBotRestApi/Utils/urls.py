from django.urls import path

from .views import *

#api/utils

urlpatterns = [
    path('audio/random_connect/get_random/', GetRandomConnectAudio.as_view(), name='get_random_audio')
]