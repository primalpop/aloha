
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
    u_name = forms.IntegerField(label="Registration Number", 
             help_text="As on your Examination ID Card")
 
    ##Application number as password    
    password = forms.CharField(label = "Application Number", 
             max_length=10, help_text="As on your Examination ID Card")
    
    dob = forms.DateField(label="Date of Birth", widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))

    def clean_username(self):
        u_name = self.cleaned_data["username"]

        ##Verifies whether username contains only digits and is not 
        ##longer than 7, i.e Username == Registration Number.
        if str(u_name).strip(digits) and len(u_name) != 7:
            msg = "Not a valid Registration Number"
            raise forms.ValidationError(msg)

        ##Verifying whether the user already exists in the database
        ##Raising error otherwise
        try:
            User.objects.get(username__exact = u_name)
            return u_name
        except User.DoesNotExist:
            raise forms.ValidationError("Registration Number doesn't exist.")

    def clean_password(self):
        pwd = self.cleaned_data['password']
        
        ##Verifying the length of application number and whether it contains
        ##only digits.

        if str(pwd).strip(digits) and len(pwd) != 5:
            msg = "Not a valid Application Number"
            raise forms.ValidationError(msg)    
        
        ##TODO: Implement the following
        ##Checking if the Application number exists in the database. Hashing it 
        ##and checking if the hash value exists.
        ##try:
        ##
        ##except DoesNotExist

    def clean_dob(self):
        dob = self.cleaned_data['dob']

        ##Getting the profile of user and verifying the entered DoB against
        ##the DoB stored in Profile.
        try:
            user = User.objects.get(username__exact = u_name)
            profile = user.get_profile()
            if profile.dob == dob:
                return dob
        except User.DoesNotExist:
            raise forms.ValidationError("Registration Number doesn't exist.")

        raise forms.ValidationError("Date of Birth doesn't match.")
        

    def clean(self):
        super(UserLoginForm, self).clean()
        ##TODO: Should the is_clean method be called on the form explicitly?
        u_name, pwd = self.cleaned_data["username"], self.cleaned_data["password"]
        user = authenticate(username = u_name, password = pwd)

        if not user:
            raise forms.ValidationError("Invalid username/password")
        return user


