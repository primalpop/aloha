from optparse import make_option
from datetime import datetime
from csv import DictReader
from django.core.management.base import BaseCommand
from allotter.models import Exam, Application, User, Profile

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--usdf',metavar='User details file name', type=str),
    )
    help = "Give the filename of the csv files that has all the details of the users"
    
    def handle(self, *args, **options):
        
        clean_users()
        
        load_users(options)
        
        self.stdout.write('Done\n')
        

def clean_users():
    """Removes all the objects from the database, required as if not done there might be a case of multiple entries"""
    User.objects.filter(is_superuser=False).delete()

def load_users(options):
    """Load option code and option name from the given csv file. The file should 
    declare a list of "exam_code,option_code,option,code".
    """
    userDetailsFileName=options.get('usdf')
    try:
        userDetailsFile = open(userDetailsFileName, 'rb')
    except IOError as (errno,strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    
        
    userReader = DictReader(userDetailsFile, delimiter=":")

    
    for data in userReader:
        appno = data['AppNo.']
        regno = data['Reg.No.']
        new_user = User.objects.create_user(regno, password=appno, email="")
        application = Application(user=new_user)
        application.np = int(data['NP'])
        if data['P1'].strip():
            application.first_paper = Exam.objects.get(exam_code=data['P1'])
            try:
                application.second_paper = Exam.objects.get(exam_code=data['P2'])
            except:
                pass
        else:
            application.first_paper = Exam.objects.get(exam_code=data['P2'])
        
            
        application.nat = data['Nat']
        application.gender = data['Gdr']
        application.cent = data['Cent']
        application.cgy = data['Cgy']
        application.save()
        dob = datetime.strptime(data['DOB'], "%d/%m/%y")
        new_profile = Profile(user=new_user, application=application)
        new_profile.dob = dob
        new_profile.save()
        print "Added user with {0} and {1} with dob as {2}".format(appno,regno,dob)