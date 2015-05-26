import django_tables2 as tables
from userprofile.models import Job
from django_tables2.utils import A  # alias for Accessor



TEMPLATE = "  <form id='delete' method='delete' action='delete/job{{job.id}}'><input type='submit' value='Delete' class='btn btn-large btn-primary' /></input></form>"

'''Creates a table containing information on  jobs
    Use this on anything were you want to display inofrmation
    on jobs, such as making a query, to seee how to do
    go to the views page and look at the jobs company_jobs funciton'''
class CompanyJobsTable(tables.Table):
    #title = tables.Column()
    args = 0
    location = tables.Column()
    level = tables.Column()
    job_type = tables.Column()
    added = tables.Column()
    title = tables.LinkColumn('job',  args=[A('id')], verbose_name='job', empty_values=())
    delete = tables.LinkColumn('delete', args=[A('id')], verbose_name='delete', empty_values=(),orderable=False)
    #delete= tables.TemplateColumn(TEMPLATE)
    class Meta:
        model = Job
        fields = ('title','location','level','job_type','added')
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
def __init__(self, *args, **kwargs):
         super(JobsTable, self).__init__(*args, **kwargs)



class AppJobsTable(tables.Table):
    company = tables.LinkColumn('company_profile', args=[A('company.id')], verbose_name='company_profile', empty_values=())
    title = tables.LinkColumn('job', args=[A('id')], verbose_name='job', empty_values=())
    location = tables.Column()
    level = tables.Column()
    job_type = tables.Column()
    added = tables.Column()


    class Meta:
        model = Job
        fields = ('company','title','location','level','job_type','added')
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
def __init__(self, *args, **kwargs):
         super(JobsTable, self).__init__(*args, **kwargs)
