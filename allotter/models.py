from django.db import models
from django.contrib.auth.models import User
from  datetime import datetime

EXAMINATION_SUBJECTS = (
    ("physics", "Physics"),
    ("mathematics", "Mathematics"),
    ("chemistry", "Chemistry"),
    )

CATEGORIES = (
    ("GEN", "GENERAL"),
    ("OBC", "OTHER BACKWARD CASTE"),
    )

OPTIONS = ( 
    ("M.Sc Chem", "M.Sc Chemisty"),
    ("M.Sc Phy", "M.Sc Physics"),
    ("M.Sc Math","M.Sc Mathematics"))

class Option(models.Model):
        opt_name = models.CharField(max_length=100, 
                verbose_name=u"Option name", 
                help_text=u"Name of Option/Stream",
                choices = OPTIONS)
        class Meta:
                verbose_name_plural = "Options"

class Exam(models.Model):
        exam_code = models.CharField(max_length=100, 
                verbose_name=u"Examination code", 
                help_text=u"Unique code for the examination")
        exam_name = models.CharField(max_length=100, 
                verbose_name=u"Examination name", 
                help_text=u"Subject name of the examination",
                choices=EXAMINATION_SUBJECTS)
        option_available = models.ForeignKey("Option",
                default=1)

        def __unicode__(self):
                return self.exam_name


class Profile(models.Model):
        user = models.OneToOneField(User)
        name = models.CharField(max_length=1024, verbose_name=u"Full Name",
                help_text=u"Name given in the application")
        roll_number = models.CharField(max_length=20,
            verbose_name=u"Examination Roll number",
            help_text=u"Roll number as per the Examination Hall ticket")
        dob = models.DateTimeField(verbose_name=u"Date of Birth",
                help_text=u"Date of birth as given in the application")
        category = models.CharField(max_length=30, choices=CATEGORIES)
        email = models.CharField(max_length=50, verbose_name=u"Email id",
            help_text=u"This will be for correspondence purposes")
        exam_taken = models.ForeignKey("Exam", default=1)


        def __unicode__(self):
                return self.name

