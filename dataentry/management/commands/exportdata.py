import csv
from django.core.management.base import BaseCommand
#from dataentry.models import Student
from django.apps import apps
import datetime
from dataentry.utils import generate_csv_file


# python manage.py exportdata model_name
class Command(BaseCommand):
    help='Export data from database to a CSV file'
    def add_arguments(self, parser):
        parser.add_argument('model_name',type=str,help='Model Name')

    def handle(self,*args,**kwargs):
        model_name=kwargs['model_name'].capitalize()

        # Search through all the apps 
        model=None
        for app_config in apps.get_app_configs():
            try:
                model=apps.get_model(app_config.label,model_name)
                break
            except LookupError:
                pass

        if not model:
            self.stderr.write(f'Model {model_name} could not found')  
            return
        # fetch data from database
        data=model.objects.all()

        # Generate csv file path
        file_path=generate_csv_file(model_name)
        
        # open the csv file and write the data
        with open(file_path,'w',newline='') as file:
            writer=csv.writer(file)

            # Write Header (print field name of model)
            writer.writerow([field.name for field in model._meta.fields])

            # write data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])
        self.stdout.write(self.style.SUCCESS('Data exported successfully !'))        