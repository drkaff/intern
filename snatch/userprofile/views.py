from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from userprofile.forms import  UserForm, UserProfileForm
def index(request):
    return render(request,'snatch/index.html',{})




def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.save()
            registered = True
        else:
            print user_form.errors,profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'snatch/register.html',
    {'user_form':user_form,'profile_form':profile_form,'registered':registered})







#A user login, need to implement more
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/snatch/')
