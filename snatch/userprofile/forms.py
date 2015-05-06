from django import forms
from userprofile.models import UserProfile
from django.contrib.auth.models import User



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('uType',)
