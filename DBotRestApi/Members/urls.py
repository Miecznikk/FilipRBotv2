from django.urls import path

from .views import *

urlpatterns = [
    path('', MemberListAPIView.as_view(), name='member-list')
]