from django.core.management.base import BaseCommand
from dataentry.models import Student
# Adding data to Database using Custom Command

class Command(BaseCommand):
    help="Insert Data to Database"

    def handle(self,*args,**kwargs):

        # Logic
        dataset=[
            {'name':'Mike','roll_no':12,'age':23},
            {'name':'John','roll_no':14,'age':21},
            {'name':'Joseph','roll_no':15,'age':25},
        ]
        for data in dataset:
           roll_no=data['roll_no']
           existing_record=Student.objects.filter(roll_no=roll_no).exists()

           if not existing_record:              
              Student.objects.create(name=data['name'], roll_no=data['roll_no'], age=data['age'])
           else:
               self.stdout.write(self.style.WARNING(f'Student with roll no {roll_no} already exists'))
        self.stdout.write(self.style.SUCCESS('Data inserted Successfully !'))

