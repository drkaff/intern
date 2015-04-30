from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return render(request,'snatch/index.html',{})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/snatch/')
