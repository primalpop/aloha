from django.db import models

from  datetime import datetime

class Option(models.Model):
        opt_name = models.CharField(max_length=100, 
                verbose_name=u"Option name", 
                help_text=u"Name of Option/Stream")
        class Meta:
                verbose_name_plural = "Options"

class Exam(models.Model):
        exam_code = models.CharField(max_length=100, 
                verbose_name=u"Examination code", 
                help_text=u"Unique code for the examination")
        exam_name = models.CharField(max_length=100, 
                verbose_name=u"Examination name", 
                help_text=u"Subject name of the examination")
        option_available = models.ForeignKey("Option",
                default=1)

        def __unicode__(self):
                return self.exam_name


class Student(models.Model):
        name = models.CharField(max_length=1024, verbose_name=u"Name",
                help_text=u"Name given in the application")
        dob = models.DateTimeField(verbose_name=u"Date of Birth",
                help_text=u"Date of birth as given in the application")
        created = models.DateTimeField(auto_now_add=True)
        exam_taken = models.ForeignKey("Exam", default=1)


        def __unicode__(self):
                return self.name

