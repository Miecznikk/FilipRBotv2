from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
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


class SetNewTimeSpentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, member_name, minutes_spent):
        member = get_object_or_404(Member, name=member_name)
        member.minutes_spent = member.minutes_spent + minutes_spent
        member.save()
        return Response({"message": "OK"}, status=status.HTTP_200_OK)


class GetTimeRankedMembersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, reqest):
        members = Member.objects.order_by('-minutes_spent')[:5]
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)


class GetPointsRankedMembersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, reqest):
        members = Member.objects.order_by('-points')[:5]
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)


class AddPointsToMember(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, member_name, points):
        member = get_object_or_404(Member, name=member_name)
        member.points += points
        member.save()
        return Response({"message": "OK"}, status=status.HTTP_200_OK)
# Create your views here.
