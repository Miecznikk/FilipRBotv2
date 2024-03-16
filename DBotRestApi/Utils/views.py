import random

from django.http import FileResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RandomConnectAudio


class GetRandomConnectAudio(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        audiofile = random.choice(RandomConnectAudio.objects.all())
        if not audiofile:
            return Response(status=404)
        audiofile = audiofile.audio_file
        return FileResponse(audiofile)

# Create your views here.
