from csv import reader
from django.core.management.base import BaseCommand, CommandError
from allotter.models import Exam

class Command(BaseCommand):
    args = '<file_name...>'
    help = "Give the filename of the csv file that has all the exam code and exam name relation"
    
    def handle(self, *args, **options):
        
        clean_exam()
        
        for fname in args:
            load_exam(fname)
        
        self.stdout.write('Done\n')
        

def clean_exam():
    """Removes all the objects from the database, required as if not done there might be a case of multile entries"""
    data = Exam.objects.all()
    data.delete()

def load_exam(filename):
    """Load exam code and exam name from the given csv file. The file should 
    declare a list of "exam_code;exam_name".
    """
    try:
        csvFile = open(filename, 'rb')
    except IOError as (errno,strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
        
    csvReader = reader(csvFile, delimiter=";")
    
    for data in csvReader:
        new_exam = Exam.objects.create()
        new_exam.exam_code = data[0]
        new_exam.exam_name = data[1]
        new_exam.save()
        print "Added ({0} : {1})".format(data[0], data[1])