from django.db import models
from django.contrib.auth.models import User

##EXAMINATION_SUBJECTS = (
##    ("Physics", "Physics"),
##    ("Mathematics", "Mathematics"),
##    ("Chemistry", "Chemistry"),
##    )

##CATEGORIES = (
##    ("GEN", "GEN"),
##    ("OBC", "OBC(Non-Creamy Layer)"),
##    ("SC", "SC"),
##    ("ST", "ST"),
##    )

##AVAILABLE_OPTIONS = ( 
##    ("MScChem", "M.Sc Chemisty"),
##    ("M.Sc-Physics-IIT-Bombay", "M.Sc Physics IIT Bombay"),
##    ("MScMath","M.Sc Mathematics"),
##	("MscHist", "M.Sc History"),
##	("MSc-PhD Dual-Degree-IIT-Bombay", "MSc-PhD Dual Degree IIT Bombay"),
##	("M.Sc Physics-IIT-Madras", "M.Sc Physics IIT Madras"),
##	("M.Sc-Physics-IIT-Guwahati", "M.Sc Physics IIT Guwahati"),
##	("M.Sc-Physics-IIT-KGP", "M.Sc Physics IIT KGP"),
##	("M.Sc-Physics-IIT-Roorkee", "M.Sc Physics IIT Roorkee"),
##)

##GENDER_CHOICES = (
##    ("M", "Male"),
##    ("F", "Female"),)

##APPLICATION_STATUS = (
##    ("I", "Incomplete"),
##    ("Submitted", "Submitted"))

##BIRTH_YEAR_CHOICES = ('1989', '1990', '1991')

class Exam(models.Model):
    """
    Table for Examination Codes and Subject names.
    """
    ##PH for Physics, CY for Chemistry
    exam_code = models.CharField(max_length=100, 
        verbose_name=u"Test Paper code", 
        help_text=u"Unique code for the Test")

    exam_name = models.CharField(max_length=100, 
        verbose_name=u"Test Paper", 
        help_text=u"Subject name of the Test")

    def __unicode__(self):
        return self.exam_name


class Option(models.Model):
    """
    Options Table, Foreign Keyed with Examination.
    """

    opt_name = models.CharField(max_length=100, 
        verbose_name=u"Programme name", 
        help_text=u"Programme Title")
	
    opt_code = models.IntegerField(max_length=3, 
		verbose_name=u"Programme Code")

    exam = models.ManyToManyField(Exam)

    class Meta:
        verbose_name_plural = "Options"
        
    def __unicode__(self):
        return self.opt_name


class Application(models.Model):
    """An application for the student - one per student
    """
    user = models.OneToOneField(User)
    
    ##To be filled by applicant
    options_selected = models.CharField(max_length=5000,help_text="CSV formatted list of options", blank=True)

	##Prefilled fields
    np = models.IntegerField(max_length=2, help_text="Number of Test Papers")

    ##Mandatory First Subject
    first_paper = models.ForeignKey(Exam, related_name="first_paper")

	##Second subject can be left blank or null
    second_paper = models.ForeignKey(Exam, related_name="second_paper", blank=True, null=True)

    nat = models.CharField(max_length=10, verbose_name="Nationality")

    gender = models.CharField(max_length=2, verbose_name="Gender")

    cent = models.IntegerField(max_length=10, verbose_name="Center Code")
	
    cgy = models.CharField(max_length=10, verbose_name="Category")

    pd = models.BooleanField(verbose_name="Physical Disability", default=False, blank=True)

    def __unicode__(self):
        u = self.user
        return u'Application for {0}'.format(u.username)

class Profile(models.Model):

    user = models.OneToOneField(User)

	#Used for verification purposes
    dob = models.DateField(verbose_name=u"Date of Birth",
        help_text=u"Date of birth as given in the application")
    
    #Application for the Profile    
    application = models.ForeignKey(Application)
	
    def __unicode__(self):
        u = self.user
        return u'User Profile {0}'.format(u.username)



