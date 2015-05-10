from django.conf.urls import patterns, url
from userprofile import views
#from registration.backends.simple.views import RegistrationView


urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$',views.user_logout, name='logout'),
    url(r'^create_job/$', views.create_job, name='create_job'),

)
