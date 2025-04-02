from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help="Greets the user"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Specifies user name')
        

    def handle(self,*args,**kwargs):
        name=kwargs['name']
        greeting = f'Hi {name}, Good Morning'
        self.stdout.write(self.style.SUCCESS(greeting))