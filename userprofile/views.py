from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from userprofile.forms import  UserForm, UserProfileForm, CreateJobForm, CreateProfileForm,NamesProfileForm, CompanyNameForm, CompanyProfileForm,ChangePasswordUserForm
from userprofile.models import UserProfile,Job
from django_tables2 import RequestConfig
from userprofile.tables import CompanyJobsTable, AppJobsTable
import os


def index(request):
    return render(request,'snatch/index.html')

def denied(request):
    return render(request,'snatch/denied.html',{})

def quiz(request):
    return render(request,'snatch/profile_quiz.html',{})

@login_required
def picture(request):
    user = User.objects.get(username = request.user)
    profile = UserProfile.objects.get(user=user)
    image = profile.profile_picture
    image = image.url[19:]
    return render(request,'snatch/picture.html',{'image':image})

@login_required
def company_profile(request,company_id):
    company = get_object_or_404(UserProfile,pk=company_id)
    user = company.user
    image = company.profile_picture
    description = company.description
    fname = user.first_name
    name = fname
    image = image.url[19:]
    return render(request,'snatch/profile.html',{'image':image,'description':description,'name':name})




@login_required
def profile(request):
    user = User.objects.get(username = request.user)
    profile = UserProfile.objects.get(user=user)
    image = profile.profile_picture
    description = profile.description
    fname = user.first_name
    lname = user.last_name
    name = fname + " " + lname
    image = image.url[19:]
    return render(request,'snatch/profile.html',{'image':image,'description':description,'name':name})

#this is a change
#A compnay's job page
@login_required
def company_jobs(request):
    user = User.objects.get(username=request.user)
    profile = UserProfile.objects.get(user=user)
    jobs = Job.objects.filter(company=profile)
    table = CompanyJobsTable(jobs)
    RequestConfig(request).configure(table)
    return render(request, 'snatch/view_jobs.html', {'table': table})

#User view jobs
@login_required
def view_jobs(request):
    jobs = Job.objects.all() #will eventually change
    table = AppJobsTable(jobs)
    RequestConfig(request).configure(table)
    return render(request, 'snatch/view_jobs.html',{'table':table, 'jobs':jobs})


#View for individual job
@login_required
def job(request,job_id):
    job = get_object_or_404(Job,pk=job_id)
    user = User.objects.get(username = request.user)
    up = UserProfile.objects.get(user=user)
    owner = False
    if(job.company == up):
        owner = True
    print owner
    return render(request,'snatch/job.html',{'job':job,'owner':owner})


#delete a job
@login_required
def delete_job(request,job_id):
    job = get_object_or_404(Job, pk=job_id).delete()
    return view_jobs(request)


@login_required
def apply_job(request,job_id):
    job = get_object_or_404(Job,pk=job_id)
    user = User.objects.get(username=request.user)
    profile = UserProfile.objects.get(user=user)
    job.applied.add(profile)
    job.save()
    return view_jobs(request)

#Registers a user
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


#Checks if user is an employee and returns true else returns false
def is_employee(user):
    u = User.objects.get(username=user)
    profile = UserProfile.objects.get(user=u)
    if(profile.user_type == "em"):
        return True
    else:
        return False

#Stores files
def handle_uploaded_file(file_path,is_resume,username):
    path = ""
    if(is_resume == True):
        path = ("userprofile/static/files/%s/resume/" % username)
    else:
        path = ("userprofile/static/files/%s/profile/" % username)
    p = str(path) + file_path.name
    if not os.path.exists(os.path.dirname(p)):
        os.makedirs(os.path.dirname(p))
    dest = open(str(p),"wb")
    for chunk in file_path.chunks():
        dest.write(chunk)
    dest.close()
    return p


@login_required
def create_user_profile(request):
    posted = False
    if request.method == "POST":
        form = CreateProfileForm(request.POST, request.FILES)
        name = NamesProfileForm(data=request.POST)
        if form.is_valid() and name.is_valid():
            res = handle_uploaded_file(request.FILES['resume'],True,request.user)
            pic = handle_uploaded_file(request.FILES['profile_picture'],False,request.user)
            f = form.save(commit=False)
            n = name.save(commit=False)
            user = User.objects.get(username = request.user)
            profile = UserProfile.objects.get(user=user)
            user.first_name = n.first_name
            user.last_name = n.last_name
            user.save()
            profile.profile_picture = pic
            profile.resume = res
            profile.description = f.description
            profile.skills = f.skills
            profile.registered = True
            profile.save()

            posted = True

        else:
            print (form.errors)
    else:
        name = NamesProfileForm()
        form = CreateProfileForm()
    return render(request,'snatch/new_user_profile.html',{'name' : name,'form':form,'posted':posted})


#Used to create a company profile
@login_required
def create_company_profile(request):
    posted = False
    if request.method == "POST":
        form = CompanyProfileForm(request.POST, request.FILES)
        name = CompanyNameForm(data=request.POST)
        if form.is_valid() and name.is_valid():
            pic = handle_uploaded_file(request.FILES['profile_picture'],False,request.user)
            f = form.save(commit=False)
            n = name.save(commit=False)
            user = User.objects.get(username = request.user)
            profile = UserProfile.objects.get(user=user)
            name =  (request.POST['company_name'])
            user.first_name = name
            user.save()
            profile.profile_picture = pic
            profile.description = f.description
            profile.registered = True
            profile.save()
            posted = True
        else:
            print (form.errors)
    else:
        name = CompanyNameForm()
        form = CompanyProfileForm()
    return render(request,'snatch/new_user_profile.html',{'name' : name,'form':form,'posted':posted})


@login_required
def create_job(request):
    posted = False
    if(is_employee(request.user)==False):
        return  HttpResponseRedirect('/snatch/denied')
    if request.method == "POST":
        form = CreateJobForm(data=request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            user = User.objects.get(username=request.user)
            profile = UserProfile.objects.get(user=user)
            f.company = profile
            f.save()
            posted = True

        else:
            print (form.errors)
    else:
        form = CreateJobForm()
    return render(request,'snatch/add_job.html',{'form':form,'posted':posted})



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
            return render(request,'snatch/signin.html',{})
    else:
            return render(request,'snatch/signin.html',{})




@login_required
def user_logout(request):

    print (request.user)
    logout(request)
    return HttpResponseRedirect('/snatch/')






@login_required
def changePassword(request):

	if request.method == 'POST':
		current_user     = request.user
		request_pass     = request.POST.get('Current')
		new_pass_1       = request.POST.get('New')
		new_pass_2       = request.POST.get('Confirm')

		if (current_user.check_password(request_pass) and new_pass_1==new_pass_2):
			request.user.set_password(new_pass_1)
			request.user.save()
			update_session_auth_hash(request, request.user)
			return render(request,'snatch/changePassword/confirm.html',{})

	return render(request,'snatch/changePassword/changePassword.html',{'change_pass_user_form':  ChangePasswordUserForm()})
