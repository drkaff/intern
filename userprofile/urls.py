from django.conf.urls import patterns, url
from userprofile import views
from userprofile.profile import changePassword
#from registration.backends.simple.views import RegistrationView


urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$',views.user_logout, name='logout'),
    url(r'^create_job/$', views.create_job, name='create_job'),
    url(r'^denied/$',views.denied,name='denied'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^company_jobs/$',views.company_jobs,name='company_jobs'),
    url(r'^jobs/$',views.view_jobs,name='view_jobs'),
    url(r'^profile/profile_quiz/$',views.quiz,name='profile_quiz'),
    url(r'^create_user_profile/$',views.create_user_profile,name='create_user_proifle'),
    url(r'^picture/$',views.picture,name='picture'),
    url(r'^create_company_profile/$',views.create_company_profile,name='create_company_proifle'),
    url(r'^job(?P<job_id>[0-9]+)/$', views.job, name='job'),
    url(r'^delete/job(?P<job_id>[0-9]+)/$',views.delete_job,name='delete'),
    url(r'^apply/job(?P<job_id>[0-9]+)/$',views.apply_job,name='apply'),
	url(r'^profile/changePassword/$',views.changePassword,name='change_password'),
    url(r'^company_profile(?P<company_id>[0-9]+)/$',views.company_profile,name='company_profile'),

)
