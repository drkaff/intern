from django import forms
from userprofile.models import UserProfile, Job
from django.contrib.auth.models import User
from userprofile.widgets import DropDownMultiple
from pygments.lexers import get_all_lexers
from pygments.lexers import get_lexer_by_name

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

#A company name form
class CompanyNameForm(forms.ModelForm):
    company_name = forms.CharField(max_length=128)
    class Meta:
        model = User
        fields = ()

# A company profile form
class CompanyProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField()
    class Meta:
        model = UserProfile
        fields = ('description','profile_picture')



class NamesProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name')


class CreateProfileForm(forms.ModelForm):

    resume = forms.FileField()
    profile_picture = forms.ImageField()
    skills =  forms.Field(widget=DropDownMultiple)


#    def __init__(self, *args, **kwargs):
#        LEXERS = [item for item in get_all_lexers() if item[1]]
#        LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
#        self.base_fields['categories'].widget.choices = LANGUAGE_CHOICES
#        super(MyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = ('skills','description','resume','profile_picture')


class ChangePasswordUserForm(forms.ModelForm):
	Current = forms.CharField(widget=forms.PasswordInput())
	New = forms.CharField(widget=forms.PasswordInput())
	Confirm = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('Current', 'New', 'Confirm')
