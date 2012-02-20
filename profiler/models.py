from django.db import models

from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('Male' : 'Male'),
    ('Female' : 'Female'),
)

SUBJECT_CHOICES = (
    ('001' : 'Physics'),
    ('002' : 'Mathematics'),
    ('003' : 'Chemistry')
)

CATEGORY_CHOICES = (
    ('GEN' : 'GENERAL'),
    ('OBC' : 'OTHER BACKWARD CASTE'),
)

class UserProfile(models.Model):
    #Mandatory field - Should be unique for an user
    user = models.ForeignKey(User, unique = True)

    #Custom fields
    exam_id = models.CharField(max_length=30, 
        verbose_name="Registration number",
        help_text = "Registration number as given in examination id card")
    
    subject = models.CharField(verbose_name="Examination Subject", 
        choices = SUBJECT_CHOICES)

    full_name = models.CharField(max_length=50, verbose_name="Full name", 
        help_text ="Name as given in application")

    dob = models.DateField(verbose_name="Date of Birth",
        help_text="YYYY-MM-DD")

    category = models.CharField(verbose_name="Category", 
        help_text="Category as given in the application",
        choices = CATEGORY_CHOICES)
        

    def __unicode__(self):
        return self.exam_id

class Notification(models.Model):
"""Borrowed from PyTask. Used to send notifications to users from the site
regarding various announcements."""

    pass

