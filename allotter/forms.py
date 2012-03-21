
from django import forms
from allotter.models import Profile
from django.forms.extras.widgets import SelectDateWidget

from django.utils.encoding import *

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from string import digits

BIRTH_YEAR_CHOICES = ('1986','1987','1988','1989','1990','1991')


class UserLoginForm(forms.Form):
    
    ##Registration Number as Username
    username = forms.IntegerField(label="Registration Number", 
             help_text="As on your Examination ID Card")
 
    ##Application number as password    
    password = forms.CharField(label = "Application Number", 
             max_length=10, help_text="As on your Examination ID Card")
    
    dob = forms.DateField(label="Date of Birth", 
            widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES),
            initial=datetime.date.today)

    def clean_username(self):
        u_name = self.cleaned_data["username"]
        
        if not u_name:
            raise forms.ValidationError("Enter an username.")    
        
        ##Verifies whether username contains only digits and is not 
        ##longer than 7, i.e Username == Registration Number.
        if str(u_name).strip(digits) or len(str(u_name)) != 7:
            msg = "Invalid Registration Number"
            raise forms.ValidationError(msg)

        ##Verifying whether the user already exists in the database
        ##Raising error otherwise
        try:
            User.objects.get(username__exact = u_name)
            return u_name
        except User.DoesNotExist:
            raise forms.ValidationError("Entered Registration Number haven't appeared for JAM Exam.")

    def clean_password(self):
    
        pwd = self.cleaned_data['password']
        
        ##Verifying the length of application number and whether it contains
        ##only digits.

        if str(pwd).strip(digits) and len(pwd) != 5:
            msg = "Not a valid Application Number"
            raise forms.ValidationError(msg)    
        
        return pwd
        
    def clean(self):
        super(UserLoginForm, self).clean()
        u_name, pwd = self.cleaned_data.get('username'), self.cleaned_data.get('password')
        dob = self.cleaned_data['dob']
        try:
            current_user = User.objects.get(username__exact = u_name)
            profile = current_user.get_profile()
            if profile.dob != dob:
                raise forms.ValidationError("Date of Birth doesn't match.")
        except User.DoesNotExist:
            raise forms.ValidationError("Correct the following errors and try logging in again.")

      
        ##Authentication part
        user = authenticate(username = u_name, password = pwd)
        if not user:
            raise forms.ValidationError("Application Number or Registration Number doesn't match.")
        return user


