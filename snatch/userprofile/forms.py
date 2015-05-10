from django import forms
from userprofile.models import UserProfile, Job
from django.contrib.auth.models import User



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_type',)

class CreateJobForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text="Enter the title of the job")
    description = forms.CharField(max_length=200,help_text="Enter a description") #description of job
    location = forms.CharField(max_length=100,help_text="Enter job location") #location of job
    class Meta:
        model = Job
        fields = ('title','description','location','level','job_type')
