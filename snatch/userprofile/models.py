import json
from smtplib import SMTP

from django.db import models
from django.contrib.auth.models import User



#User Profile page
class UserProfile(models.Model):
    #The profile types of every user
    PROFILE_TYPES = (
        ('em','Employer'),
        ('ap','Applicant'),
     )
     #contains username,first_name,last_name,email,and password
    user = models.OneToOneField(User) #uses the django usertype
    uType = models.CharField(max_length=2,
                              choices=PROFILE_TYPES)
    skills = models.CharField(max_length=300,default=None)

    #return the type of user, either intern or employer
    def user_type(self):
        return self.uType

    #Get user email
    def get_email(self):
        return self.user.email

    #return the username of a user
    def get_username(self):
        return self.user.username


    def __str__(self):
         return self.user.username

    #get user skills, skills is a string and must be converted to list
    def get_skills(self):
        if (self.skills is not None):
            jsonDec = json.decoder.JSONDecoder()
            skillsList = jsonDec.decode(self.skills) #convert string to list
            return skillsList
        else:
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
        server = smtplib.SMTP("smtp.gmail.com",587) #gmail server
        server.starttls() #connect to server
        server.login('snatchtest1@gmail.com','password0864')  #login to server
        try:
            server.sendmail('Snatch',self.user.email,message) # send message
        finally:
            server.close() #disconnect from server




#A job class
class job(models.Model):

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

    company = models.ForeignKey(UserProfile) #A company owns the job posting
    title = models.CharField(max_length=100,default=None) #title of job
    description = models.CharField(max_length=200,default=None) #description of job
    location = models.CharField(max_length=100,default=None) #location of job
    skills = models.CharField(max_length=300,default=None)#list of skills
    added = models.DateTimeField(auto_now_add=True) #when job was listed
    applied = models.ManyToManyField(UserProfile) #many user can apply to job
    level = models.CharField(max_length=2) #level of job
    job_type = models.CharField(max_length=2) #type of job


    def __str__(self):
        return self.title

    def get_desription(self):
        return self.description

    def get_company(self):
        return self.company

    def get_location(self):
        return self.loaction

    def get_skills(self):
        return self.skills

    def get_added(self):
        return self.added

    def get_applied(self):
        return self.applied
