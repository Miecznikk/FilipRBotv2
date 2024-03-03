from django.urls import path

from .views import *

urlpatterns = [
    path('', MemberListAPIView.as_view(), name='member-list'),
    path('roles/gameroles/', GameRolesListAPIView.as_view(), name='game-roles-list')
]