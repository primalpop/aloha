from django import forms
from allotter.models import Profile
from django.forms.extras.widgets import SelectDateWidget

from django.utils.encoding import *

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from string import digits, uppercase

BIRTH_YEAR_CHOICES = tuple(range(1960, 1994, 1))
DD_YEAR_CHOICES = (2011, 2012)


class UserLoginForm(forms.Form):
    
    ##Registration Number as Username
    username = forms.IntegerField(label="Registration Number", 
             help_text="As on your Examination Admit Card")
 
    ##Application number as password    
    password = forms.CharField(label = "Application Number", 
             max_length=10, help_text="As on your Examination Admit Card")
    
    dob = forms.DateField(label="Date of Birth", 
            widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES, attrs={"class":"span1"}),
            initial=datetime.date.today)
    
    dd_no = forms.CharField(label="Demand Draft Number",
            max_length=10, help_text="Valid DD Number")
    
    dd_date = forms.DateField(label="Date of Issue",
            help_text="Please ensure that Demand Draft is valid",
            widget=SelectDateWidget(years=DD_YEAR_CHOICES, attrs={"class":"span1"}),
            initial=datetime.date.today)
                            
    dd_amount = forms.IntegerField(label="Amount", 
                help_text="As mentioned on the brochure.")
    
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
        dob = self.cleaned_data["dob"]
        dd_no = self.cleaned_data.get("dd_no")
        dd_date = self.cleaned_data.get("dd_date")
        dd_amount = self.cleaned_data.get("dd_amount")
        try:
            current_user = User.objects.get(username__exact = u_name)
            profile = current_user.get_profile()
            if profile.dob != dob:
                raise forms.ValidationError("Date of Birth doesn't match.")
        except User.DoesNotExist:
            raise forms.ValidationError("Correct the following errors and try logging in again.")

        ##Validating the DD Details
        
        if dd_no and dd_amount:
            if dd_no.strip(digits+uppercase):
                raise forms.ValidationError("Not a valid Demand Draft Number")
            elif dd_amount != 300:
                raise forms.ValidationError("Make sure the amount matches what is mentioned in brochure")
                  
        else:
            raise forms.ValidationError("Fill in the Demand Draft Details")
      
        ##Authentication part
        user = authenticate(username = u_name, password = pwd)
        user_profile = user.get_profile()
        user_profile.dd_no = dd_no
        user_profile.save()
        if not user:
            raise forms.ValidationError("Application Number or Registration Number doesn't match.")
        return user
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-loginform'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = " "
        self.helper.add_input(Submit('submit', 'Submit'))
        super(UserLoginForm, self).__init__(*args, **kwargs)


class UserDetailsForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.helper = FormHelper()
        self.helper.form_id = 'id-detailsform'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = "/allotter/"+user.username+"/details/"
        self.helper.add_input(Submit('submit', 'Submit'))
        super(UserDetailsForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label="Email Address", widget=forms.TextInput(attrs={"placeholder":"john@example.com",}),
                help_text="Enter a valid email id where you will able to receive correspondence from JAM 2012.")
    phone_number = forms.CharField(label="Phone number", max_length=15, widget=forms.TextInput(attrs={"placeholder":"9876543210",}), help_text="Phone number with code")
    
    cat_check = forms.BooleanField(required=False, initial=False, label="Check this if you belong to SEBC Category")

    def clean_phone_number(self):
        pno = self.cleaned_data['phone_number']
        if str(pno).strip(digits):
            raise forms.ValidationError("Not a valid phone number")
        return pno  
        
    def save(self):  
        cleaned_data = self.cleaned_data
        user_profile = self.user.get_profile()
        
        email = self.cleaned_data['email']
        phone_number = self.cleaned_data['phone_number']
        cat_check = self.cleaned_data['cat_check']
           
        if email and phone_number:
            user_profile.secondary_email = email
            user_profile.phone_number = phone_number
            
        if cat_check:    
            user_profile.cat_status = True
            
        else:
            raise forms.ValidationError("Make sure that you have entered all the details.")    

        user_profile.save()
        
        
