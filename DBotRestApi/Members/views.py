from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Member, GameRole
from .serializers import MemberSerializer, GameRoleSerializer


class MemberListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)


class GameRolesListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        game_roles = GameRole.objects.all()
        serializer = GameRoleSerializer(game_roles, many=True)
        return Response(serializer.data)


class GameRoleGetAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, game_detection_string):
        game_role = GameRole.objects.filter(game_detection_string__contains=game_detection_string)
        if len(game_role) > 1 or len(game_role) == 0:
            raise Http404("Multiple objects found")
        serializer = GameRoleSerializer(game_role, many=True)
        return Response(serializer.data)
# Create your views here.
