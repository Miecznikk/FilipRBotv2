from django.urls import path

from .views import *

# /api/members

urlpatterns = [
    path('', MemberListAPIView.as_view(), name='member-list'),
    path('roles/gameroles/', GameRolesListAPIView.as_view(), name='game-roles-list'),
    path('roles/gameroles/<str:game_detection_string>/', GameRoleGetAPIView.as_view(), name='game-role-get'),
    path('minutes_spent/<str:member_name>/<int:minutes_spent>/', SetNewTimeSpentAPIView.as_view(), name='set-new'
                                                                                                        '-minutes'),
    path('points/add/<str:member_name>/<int:points>/', AddPointsToMember.as_view(), name='add-points'),
    path('minutes_spent/ranking/', GetTimeRankedMembersAPIView.as_view(), name='time-ranking'),
    path('points/ranking/', GetPointsRankedMembersAPIView.as_view(), name='points-ranking')
]
