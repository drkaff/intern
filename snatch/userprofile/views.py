from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from userprofile.forms import  UserForm, UserProfileForm, CreateJobForm
from django.shortcuts import get_object_or_404
from userprofile.models import UserProfile
from django import template
def index(request):
    return render(request,'snatch/index.html',{})




def register(request):

    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            username = request.POST.get('username')
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            x = UserProfile.objects.get(user = user)
            x.user_type = profile.user_type
            x.save()
            registered = True

        else:
            print (user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'snatch/register.html',
    {'user_form':user_form,'profile_form':profile_form,'registered':registered})


#Create a Job posting
@login_required
def create_job(request):
    if request.method == "POST":
        form = CreateJobForm(data=request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            user = User.objects.get(username=request.user)
            profile = UserProfile.objects.get(user=user)
            f.company = profile
            f.save()

        else:
            print (form.errors)
    else:
        form = CreateJobForm()
    return render(request,'snatch/add_job.html',{'form':form})



#A user login, need to implement more
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:
            if  user.is_active:
                login(request,user)
                return HttpResponseRedirect('/snatch/')
            else:
                return HttpResponse("Your snatch account is disabled")
        else:
            print ("Invalid login details: {0}, {1}".format(username,password))
            return HttpResponse("Invalid login details supplied.")
    else:
            return render(request,'snatch/login.html',{})


@login_required
def user_logout(request):

    print (request.user)
    logout(request)
    return HttpResponseRedirect('/snatch/')
