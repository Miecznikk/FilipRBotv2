import os

from django.core.management.base import BaseCommand

from DBotRestApi import settings
from Responses.models import DefaultUserRelatedMessage
from Members.models import Member


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('member_name')
        parser.add_argument('file_name')

    def handle(self, *args, **options):
        member_name = options['member_name']
        file_name = os.path.join(f'{settings.BASE_DIR}/Responses/management/commands/', options['file_name'])
        try:
            member = Member.objects.get(name=member_name)
            try:
                with open(file_name, 'r') as file:
                    lines = [line[:-1] for line in file]
                for line in lines:
                    DefaultUserRelatedMessage.objects.create(user=member, description=line)
            except FileNotFoundError:
                print(f"File {file_name} not found")
                return
        except Member.DoesNotExist:
            print(f"Member {member_name} does not exist")
            return
