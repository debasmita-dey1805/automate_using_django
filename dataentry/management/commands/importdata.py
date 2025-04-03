from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
from django.db import DataError
# python manage.py importdata file_path model_name

class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Name of the Model')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        # Search for the model in all installed apps
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)  # Fix: use model_name
                break
            except LookupError:
                continue  # Model not found, continue searching in the next app

        if not model:
            raise CommandError(f'Model "{model_name}" not found in any app!')
        
        
        # get all the fields name of the model that we found
        model_fields=[field.name for field in model._meta.fields if field.name !='id']
        print(model_fields)

        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                csv_header=reader.fieldnames

                # Compare uploaded CSV header with model's field name
                if csv_header !=model_fields:
                    raise DataError(f"CSV file doesn't match with the {model_name} table fields")

                for row in reader:
                    model.objects.create(**row)

            self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))
        
        except Exception as e:
            raise CommandError(f'Error importing data: {e}')
