
from django import forms
from allotter.models import Profile
from django.forms.extras.widgets import SelectDateWidget

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from string import digits, letters, punctuation

from allotter.models import BIRTH_YEAR_CHOICES, GENDER_CHOICES, EXAMINATION_SUBJECTS, CATEGORIES

PWD_CHARS = letters + punctuation + digits

class RegistrationForm(forms.Form):
    #5 Digit Registration Number would be used as username
    username = forms.IntegerField(help_text="Enter your Registration Number")
    
    password = forms.CharField(max_length=30,
        widget=forms.PasswordInput())
    
    confirm_password = forms.CharField(max_length=30,
        widget=forms.PasswordInput())

    email = forms.EmailField()

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    app_no = forms.IntegerField(help_text="Enter your Application Number")

    exam_code = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        choices=EXAMINATION_SUBJECTS,
        help_text="Options available depends on the qualified Exam")
   
    #All India Rank
    air = forms.DecimalField(help_text="All India Rank")
    
    dob = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES)
    category = forms.ChoiceField(widget=forms.RadioSelect, choices=CATEGORIES)
    
    #Physical Disability
    pd = forms.BooleanField()
    

    def clean_username(self):
        u_name = self.cleaned_data["username"]
        
        if str(u_name).strip(digits) and len(u_name) != 7:
            msg = "Not a valid Registration Number"
            raise forms.ValidationError(msg)

        try:
            User.objects.get(username__exact = u_name)
            raise forms.ValidationError("Registration Number already exists.")
        except User.DoesNotExist:
            return u_name

        
    def clean_password(self):  
        pwd = self.cleaned_data['password']
        if pwd.strip(PWD_CHARS):
            raise forms.ValidationError("Only letters, digits and punctuation \
            are allowed in password")

    def clean_confirm_password(self):
        c_pwd = self.cleaned_data['confirm_password']
        pwd = self.data['password']
        if c_pwd != pwd:
            raise forms.ValidationError("Passwords do not match")

        return c_pwd

	def save(self):
		u_name = self.cleaned_data["username"]
		pwd = self.cleaned_data["password"]
		email = self.cleaned_data['email']
		new_user = User.objects.create_user(u_name, email, pwd)

        new_user.first_name = self.cleaned_data["first_name"]
        new_user.last_name = self.cleaned_data["last_name"]
        new_user.save()
        cleaned_data = self.cleaned_data
        new_profile = Profile(user=new_user)
        new_profile.exam_code = cleaned_data["exam_code"]
        new_profile.gender = cleaned_data["gender"]
        new_profile.rank = cleaned_data["air"]
        new_profile.category = cleaned_data["category"]
        new_profile.dob = cleaned_date["dob"]
        new_profile.application_number = cleaned_data["app_no"]
        new_profile.save()

        return u_name, pwd

class UserLoginForm(forms.Form):
    username = forms.IntegerField(help_text="Registration Number of Applicant")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(), 
        help_text="Keep it safe")

    def clean(self):
        super(UserLoginForm, self).clean()
        u_name, pwd = self.cleaned_data["username"], self.cleaned_data["password"]
        user = authenticate(username = u_name, password = pwd)

        if not user:
            raise forms.ValidationError("Invalid username/password")

        return user

