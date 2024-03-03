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
# Create your views here.
