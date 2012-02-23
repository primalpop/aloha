from django.db import models
from django.contrib.auth.models import User

from  datetime import datetime

EXAMINATION_SUBJECTS = (
    ("phy", "Physics"),
    ("math", "Mathematics"),
    ("chem", "Chemistry"),
    )

CATEGORIES = (
    ("GEN", "GENERAL"),
    ("OBC", "OTHER BACKWARD CASTE"),
    )

AVAILABLE_OPTIONS = ( 
    ("MScChem", "M.Sc Chemisty"),
    ("MScPhy", "M.Sc Physics"),
    ("MScMath","M.Sc Mathematics"))

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"))

APPLICATION_STATUS = (
    ("I", "Incomplete"),
    ("Submitted", "Submitted"))


class Option(models.Model):

    opt_name = models.CharField(max_length=100, 
        verbose_name=u"Option name", 
        help_text=u"Name of Option/Stream",
        choices = AVAILABLE_OPTIONS)

    seats = models.IntegerField(verbose_name=u"Seats available")

    class Meta:
        verbose_name_plural = "Options"
        
    def __unicode__(self):
        return self.opt_name


class Exam(models.Model):

    exam_code = models.CharField(max_length=100, 
        verbose_name=u"Examination code", 
        help_text=u"Unique code for the examination")

    exam_name = models.CharField(max_length=100, 
        verbose_name=u"Examination name", 
        help_text=u"Subject name of the examination",
        choices=EXAMINATION_SUBJECTS)

    def __unicode__(self):
        return self.exam_name


class Profile(models.Model):

    user = models.OneToOneField(User)

    roll_number = models.CharField(max_length=20,
        verbose_name=u"Examination Roll number",
        help_text=u"Roll number as per the Examination Hall ticket")

    dob = models.DateTimeField(verbose_name=u"Date of Birth",
        help_text=u"Date of birth as given in the application")

    category = models.CharField(max_length=30, choices=CATEGORIES)

    def __unicode__(self):
        return self.name

class Application(models.Model):
    """An application for the student - one per student
    """
    user = models.ForeignKey(User)

    profile = models.ForeignKey(Profile)

    #To be modified to include multiple subjects for a student
    exam_taken = models.ForeignKey(Exam)
    
    #All options chosen
    options = models.ManyToManyField(Option)

    status = models.CharField(max_length=24, choices=APPLICATION_STATUS)

    editable = models.BooleanField(default=True)

    def __unicode__(self):
        u = self.user
        return u'Application for {0} {1}'.format(u.first_name, u.last_name)

