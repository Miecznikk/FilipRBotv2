from rest_framework import serializers
from .models import Member, GameRole


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'points', 'minutes_spent', 'configurator']


class GameRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRole
        fields = ['name', 'game_assigned', 'game_detection_string']
