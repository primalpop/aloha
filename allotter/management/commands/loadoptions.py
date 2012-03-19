import argparse
from csv import reader
from django.core.management.base import BaseCommand, CommandError
from allotter.models import Exam, Option

class Command(BaseCommand):
    args = '<file_name...>'
    help = "Give the filename of the csv file that has all the option code, name and exam code relation"
    
    def handle(self, *args, **options):
        
        clean_option()
        
        parser = argparse.ArgumentParser(description='Process some integers.')

        parser.add_argument('-pcc',metavar='Paper course code file name', type=str)
        parser.add_argument('-cc',metavar='Course code file name', type=str)

        args = parser.parse_args()
        
        load_option(vars(args)['pcc'])
        
        self.stdout.write('Done\n')
        

def clean_option():
    """Removes all the objects from the database, required as if not done there might be a case of multiple entries"""
    data = Option.objects.all()
    data.delete()

def load_option(filename):
    """Load option code and option name from the given csv file. The file should 
    declare a list of "exam_code,option_code,option,code".
    """
    try:
        csvFile = open(filename, 'rb')
    except IOError as (errno,strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
        
    csvReader = reader(csvFile, delimiter=",")
    
    for data in csvReader:
        exam = Exam.objects.get(exam_code=data[0])
        for value in data[1:len(data)]:
            try:
                new_option = Option.objects.get(opt_code=value)
            except Option.DoesNotExist:
                new_option = Option(opt_name="Test",opt_code=value)
                new_option.save()
            new_option.exam.add(exam)
            print "Added (option Test with code {0} and exam {1})".format(value,exam)
