from django.urls import path

from .views import *


urlpatterns = [
    path('get/default_message/<str:user_name>/<str:message_content>', GetDefaultMessageView.as_view(), name='get-default-message')
]