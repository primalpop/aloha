from csv import writer
from django.core.management.base import BaseCommand
from allotter.models import Application

class Command(BaseCommand):
    help = "Give the filename of the csv files that has all the details of the users"
    
    def handle(self, *args, **options):
        
        dump_csv()
        
        self.stdout.write('Done\n')
        
def dump_csv():
    application = Application.objects.all()    
    csvWriter = writer(open('csvdump.csv', 'w'), delimiter=":")
    csvWriter.writerow(['RegNo.','np','option_selected'])
    for users in application:
        csvWriter.writerow([users.user, users.np, users.options_selected])

