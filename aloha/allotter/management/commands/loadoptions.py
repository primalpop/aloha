from optparse import make_option
from csv import reader
from django.core.management.base import BaseCommand
from allotter.models import Exam, Option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--pcc',metavar='Paper course code eligibility file name', type=str),
        make_option('--cc',metavar='Course code file name', type=str),
    )
    help = "Give the filenames of the csv files that has all the option code, name and exam code relation"
    
    def handle(self, *args, **options):
        
        clean_option()
        
        load_option(options)
        
        self.stdout.write('Done\n')
        

def clean_option():
    """Removes all the objects from the database, required as if not done there might be a case of multiple entries"""
    data = Option.objects.all()
    data.delete()

def load_option(options):
    """Load option code and option name from the given csv file. The file should 
    declare a list of "exam_code,option_code,option,code".
    """
    paperCourseFileName=options.get('pcc')
    courseCodeFileName=options.get('cc')
    try:
        paperCourseFile = open(paperCourseFileName, 'rb')
    except IOError as (errno,strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    
    try:
        courseCodeFile = open(courseCodeFileName, 'rb')
    except IOError as (errno,strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
        
    paperReader = reader(paperCourseFile, delimiter=":")
    courseReader = reader(courseCodeFile, delimiter=":")
    
    courseDict = {}
    
    for data in courseReader:                                                   
        courseDict[int(data[0])]=[data[1],data[2]]
    
    for data in paperReader:
        exam = Exam.objects.get(exam_code=data[0])
        for value in data[1:len(data)]:
            try:
                new_option = Option.objects.get(opt_code=value)
            except Option.DoesNotExist:
                new_option = Option(opt_name=courseDict[int(value)][0],opt_code=value, opt_location=courseDict[int(value)][1])
                new_option.save()
            new_option.exam.add(exam)
            print "Added (option {0} with code {1} at {3} and exam {2})".format(courseDict[int(value)][0],value,exam,courseDict[int(value)][1])
