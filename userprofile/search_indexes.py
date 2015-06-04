import datetime
from haystack import indexes
from userprofile.models import Job
from django.utils import timezone
class JobIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True) #title of job
    company = indexes.CharField(model_attr='company') #A company owns the job posting
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description') #description of job
    location = indexes.CharField(model_attr='location') #location of job
    skills = indexes.CharField(model_attr='skills')#list of skills
    level = indexes.CharField(model_attr='level') #level of job
    job_type = indexes.CharField(model_attr='job_type') #type of job


    def get_model(self):
        return Job
'''
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(added=timezone.now())'''
