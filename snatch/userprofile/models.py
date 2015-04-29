import json
from smtplib import SMTP

from django.db import models
from django.contrib.auth.models import User



#User Profile page
class UserProfile(models.Model):
    #The profile types of every user
    PROFILE_TYPES = (
        ('in','Intern'),
        ('em','Employer'),
     )
     #contains username,first_name,last_name,email,and password
    user = models.OneToOneField(User)
    uType = models.CharField(max_length=2,
                              choices=PROFILE_TYPES)
    skills = models.CharField(max_length=300,default=None)

    #return the type of user, either intern or employer
    def user_type(self):
        return self.uType

    #Get user email
    def get_email(self):
        return self.user.email

    def __str__(self):
         return self.user.username #return the username of a user

    #get user skills, skills is a string and must be converted to list
    def get_skills(self):
        if (self.skills is not None):
            jsonDec = json.decoder.JSONDecoder()
            skillsList = jsonDec.decode(self.skills) #convert string to list
            return skillsList
        else:
            return None

    #add to skills have to call get skills to get array and then add to it and return to string
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
        server.sendmail('Snatch',self.user.email,message) # send message
        server.close() #disconnect from server
