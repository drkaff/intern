import json
from smtplib import SMTP
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from pygments.lexers import get_all_lexers
from pygments.lexers import get_lexer_by_name

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])

def upload_to_img(instance, filename):
    return 'userprofile/static/files/%s/profile/%s' % (instance.user.username, filename)
def upload_to_res(instance, filename):
    return 'userprofile/static/files/%s/resume/%s' % (instance.user.username, filename)
#User Profile page
class UserProfile(models.Model):
    #The profile types of every user
    PROFILE_TYPES = (
        ('em','Employer'),
        ('ap','Applicant'),
     )
     #contains username,first_name,last_name,email,and password
    user = models.OneToOneField(User) #uses the django usertype
    user_type = models.CharField(max_length=2,
                              choices=PROFILE_TYPES,default="")
    skills = models.CharField(max_length=300)#list of skills
    description = models.CharField(max_length=300,default="")
    resume = models.FileField(null=True,upload_to=upload_to_img) #holds the resume
    profile_picture = models.ImageField(default='static/files/default.jpeg',upload_to=upload_to_res)
    registered = models.BooleanField(default=False)
    culture = models.CharField(max_length=200)
    quiz = models.CharField(max_length=50)    #get user skills, skills is a string and must be converted to list
    def get_skills(self):
        if (self.skills is not None):
            skills = self.skills
            skills = str(skills)
            skills = skills.replace(' ','')
            skills = skills.split(',')
            skills.pop()
            return skills

        return None

    #add to skills have to call get skills to get array
    #and then add to it and return to string
    #array of skills added to skill_list
    def add_skills(self,skills):
        skills_list = self.get_skills() #get skill list as list
        if skills_list is None:
            skills_list = []
        for skill in skills:
            skill_lists = skills_list.append(skill) # add item to list
        sk = json.dumps(skills_list) #convert list to string
        self.skills = sk

    #send an email to the user
    def send_email(self,message):
        server = SMTP("smtp.gmail.com",587) #gmail server
        server.starttls() #connect to server
        server.login('snatchtest1@gmail.com','password12345!')  #login to server
        try:
            server.sendmail('Snatch',self.user.email,message) # send message
        finally:
            server.close() #disconnect from server

    def __str__(self):
        name = ""
        name += self.user.first_name
        lname = self.user.last_name
        if(lname != ""):
            name+=lname
        return name

    def get_absolute_url(self):
        return "/snatch/profile%s" % self.id


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

#A job class
class Job(models.Model):

    #Job level type
    JOB_LEVEL = (
        ('in','Internship'),
        ('en','Entry'),
        ('ju','Junior'),
        ('mi','Mid'),
        ('se','Senior'),
    )

    #Job length type
    JOB_TYPE = (
        ('in','Internship'),
        ('fl','Full Time'),
        ('pt','Part Time'),
        ('ct','Contract'),
    )
    #TO DO: ADD PERSONALITY TRAIT/TYPE


    company = models.ForeignKey(UserProfile,related_name = 'company') #A company owns the job posting
    title = models.CharField(max_length=100,default="") #title of job
    description = models.CharField(max_length=200,default="") #description of job
    location = models.CharField(max_length=100,default="") #location of job
    skills = models.CharField(max_length=300,choices=LANGUAGE_CHOICES)#list of skills
    added = models.DateTimeField(auto_now_add=True) #when job was listed
    applied = models.ManyToManyField(UserProfile,related_name = 'applicants') #many user can apply to job
    level = models.CharField(max_length=2,choices=JOB_LEVEL) #level of job
    job_type = models.CharField(max_length=2,choices=JOB_TYPE) #type of job
    culture = models.CharField(max_length=200)
    quiz = models.CharField(max_length=50)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return "/snatch/job%s" % self.id
