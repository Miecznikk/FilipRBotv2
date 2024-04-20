import os

from django.core.management.base import BaseCommand

from DBotRestApi import settings
from django.apps import apps


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('class_name')
        parser.add_argument('file_name')

    def handle(self, *args, **options):
        class_name = options['class_name']
        file_name = os.path.join(f'{settings.BASE_DIR}/Responses/management/commands/', options['file_name'])
        try:
            model_class = apps.get_model(app_label="Responses", model_name=class_name)
            try:
                with open(file_name, 'r') as file:
                    lines = [line[:-1] for line in file]
                for line in lines:
                    model_class.objects.create(description=line)
            except FileNotFoundError:
                print(f'File {file_name} not found')
        except LookupError:
            print(f"Class name {class_name} not found")
            return
