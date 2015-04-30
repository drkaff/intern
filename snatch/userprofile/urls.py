from django.conf.urls import patterns, url
from userprofile import views
from registration.backends.simple.views import RegistrationView


urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
)
