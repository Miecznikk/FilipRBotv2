from django.core.management.base import BaseCommand
from Responses.models import DefaultUserRelatedMessage
from Members.models import Member

class Command(BaseCommand):
    def handle(self, *args, **options):
        member = Member.objects.get(name="miecznikk")
        lines = []
        with open("Responses/management/commands/tmp.txt", "r") as file:
            lines = [line for line in file]

        print(lines)

