import os

from django.core.management.base import BaseCommand

from DBotRestApi import settings
from Responses.models import RoleDefaultMessage
from Members.models import Role


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('role_name')
        parser.add_argument('file_name')

    def handle(self, *args, **options):
        role_name = options['role_name']
        file_name = os.path.join(f'{settings.BASE_DIR}/Responses/management/commands/', options['file_name'])
        try:
            role = Role.objects.get(name=role_name)
            try:
                with open(file_name, 'r') as file:
                    lines = [line[:-1] for line in file]
                for line in lines:
                    RoleDefaultMessage.objects.create(role=role, description=line)
            except FileNotFoundError:
                print(f'File {file_name} not found')
        except Role.DoesNotExist:
            print(f'Role {role_name} not found.')
