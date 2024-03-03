from django.contrib import admin
from .models import Role, Member, GameRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(GameRole)
class GameRoleAdmin(admin.ModelAdmin):
    list_display = ['game_assigned']
