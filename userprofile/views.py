from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from userprofile.forms import  *
from userprofile.models import UserProfile,Job
from django_tables2 import RequestConfig
from userprofile.tables import CompanyJobsTable, AppJobsTable
from smtplib import SMTP
import os
from pygments.lexers import get_all_lexers
from pygments.lexers import get_lexer_by_name
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
def test(request):
    items =  ['Efficient','Multi-tasker','Problem Solver','Punctual','Research',
              'Planning','Leading','Teamwork','Client Relationships','Sales',
              'Administration','Bookkeeping','Lecture','Human Resource Management']
    return render(request,'snatch/test.html',{'items':items})


def index(request):
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user)
        up = UserProfile.objects.get(user=user)
        if(up.registered == True):
            return profile(request,user.id)
        else:
            return render(request,'snatch/index.html')
    else:
        return render(request,'snatch/home.html')

def denied(request):
    return render(request,'snatch/denied.html',{})

def legal(request):
	return render(request,'snatch/legal.html')

@csrf_exempt
def quiz(request):
    if request.method == "POST":
        quizno = request.POST.get('quizno')
        # INSERT QUIZNO INTO USER PROFILE COLUMN
        return HttpResponse("%s" % quizno)
    else:
        return render(request,'snatch/profile_quiz.html',{})

@login_required
def company_profile(request,company_id):
    access = User.objects.get(username=request.user)
    owner = False
    if(access.id == company_id):
        owner = True
    company = get_object_or_404(UserProfile,pk=company_id)
    user = company.user
    image = company.profile_picture
    description = company.description
    fname = user.first_name
    name = fname
    image = image.url[19:]
    email = user.email
    pid = company_id
    return render(request,'snatch/profile.html',{'image':image,'description':description,'name':name,'company':company,'company_id':company_id,'owner':owner,'email':email,'pid':pid})


@login_required
def profile(request,user_id):
    access = User.objects.get(username=request.user)
    user = User.objects.get(pk=user_id)
    profile = UserProfile.objects.get(user=user)
    email = user.email
    pid = profile.id
    owner = False
    if(access.id == user_id):
        owner = True
    image = profile.profile_picture
    description = profile.description
    name = user.first_name + " " + user.last_name
    image = image.url[19:]
    skills = profile.skills
    skills = skills.split(',')
    skills = skills
    is_company = profile.user_type
    print request.method
    if(owner == False):
        if request.method == 'POST':
            message = request.POST.get("message")
            if(message != ""):
                send_email(email,message)
    if(is_company=="em"):
        company = True
    else:
        company = False
    return render(request,'snatch/profile.html',{'image':image,'description':description,'name':name,'company':company,'skills':skills,'pid':pid,'owner':owner,'email':email})



#this is a change
#A compnay's job page
@login_required
def company_jobs(request,company_id):
    profile = UserProfile.objects.get(pk=company_id)
    jobs = Job.objects.filter(company=profile)
    table = CompanyJobsTable(jobs)
    RequestConfig(request).configure(table)
    print company_id
    return render(request, 'snatch/view_jobs.html', 'snatch/profile.hmtl', {'table': table,'company_id':company_id})

@login_required
def company_only_jobs(request):
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

#view applied to jobs
@login_required
def view_applied(request,user_id):
    user = User.objects.get(id=user_id)
    profile = UserProfile.objects.get(user=user)
    jobs = Job.objects.all().filter(applied=profile)
    table = AppJobsTable(jobs)
    pid = user_id
    return render(request, 'snatch/view_jobs.html',{'table':table, 'jobs':jobs,'pid':pid})

def view_users_applied(request,job_id):
    job = Job.objects.get(pk=job_id)
    users = job.applied.all()
    return render(request, 'snatch/applied_to.html',{'users':users})


#View for individual job
@login_required
def job(request,job_id):
    job = get_object_or_404(Job,pk=job_id)
    user = User.objects.get(username = request.user)
    up = UserProfile.objects.get(user=user)
    owner = False
    if(job.company == up):
        owner = True
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
    update = False
    posted = False
    title = "Create Profile"
    languages = getLanguages()
    if request.method == "POST":
        form = CreateProfileForm(request.POST, request.FILES)
        name = NamesProfileForm(data=request.POST)
        languages = getLanguages()
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
    return render(request,'snatch/new_user_profile.html',{'name' : name,'form':form,'posted':posted,'title':title,'update':update,'languages':languages})


def getLanguages():
    LEXERS = [item for item in get_all_lexers() if item[1]]
    LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
    languages = []
    for i in LANGUAGE_CHOICES:
        languages.append("%s" % i[0])
    return languages

@login_required
def update_profile(request):
    user = User.objects.get(username=request.user)
    profile = UserProfile.objects.get(user=user)
    if(profile.user_type=="em"):
        return update_company_profile(request)
    elif(profile.user_type=="ap"):
        return update_user_profile(request)

@login_required
def update_user_profile(request):
    update = True
    user = User.objects.get(username=request.user)
    profile = UserProfile.objects.get(user=user)
    form = CreateProfileForm()
    posted = False
    title = "Update Profile"
    languages = getLanguages()
    userSkills = profile.skills
    if request.method == "POST":
        form = CreateProfileForm(request.POST,instance=profile)
        name = NamesProfileForm(data=request.POST,instance=user)
        if form.is_valid() and name.is_valid():
            skills = request.POST.get('skills')
            profile.skills = skills
            f = form.save()
            n = name.save()
            profile.save()
            posted = True
            return index(request)

        else:
            print (form.errors)
    else:
        name = NamesProfileForm()
        form = UpdateProfileForm()
        name.fields['first_name'].initial = user.first_name
        name.fields['last_name'].initial = user.last_name
        form.fields["description"].initial = profile.description


    return render(request,'snatch/update_user_profile.html',{'name' : name,'form':form,'posted':posted,'title':title,'update':update,'languages':languages,'userSkills':userSkills})


@login_required
def update_company_profile(request):
    update = True
    user = User.objects.get(username = request.user)
    profile = UserProfile.objects.get(user=user)
    posted = False
    if request.method == "POST":
        form = EditCompanyProfileForm(request.POST,instance=profile)
        name = CompanyNameForm(data=request.POST,instance=user)
        if form.is_valid() and name.is_valid():
            n = name.save(commit=False)
            f = form.save()
            name =  (request.POST['company_name'])
            user.first_name = name
            user.save()
            posted = True
            return index(request)
        else:
            print (form.errors)
    else:
        name = CompanyNameForm()
        form = EditCompanyProfileForm()
        name.fields['company_name'].initial = user.first_name
        form.fields['description'].initial = profile.description
    return render(request,'snatch/update_user_profile.html',{'name' : name,'form':form,'posted':posted,'update':update})

#Used to create a company profile
@login_required
def create_company_profile(request):
    posted = False
    update = False
    if request.method == "POST":
        form = CompanyProfileForm(request.POST, request.FILES)
        name = CompanyNameForm(data=request.POST)
        print "HERE"
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
    return render(request,'snatch/new_user_profile.html',{'name' : name,'form':form,'posted':posted,'update':update})


@login_required
def create_job(request):
    posted = False
    states = getStates()
    if(is_employee(request.user)==False):
        return  HttpResponseRedirect('/snatch/denied')
    if request.method == "POST":
        form = CreateJobForm(data=request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            user = User.objects.get(username=request.user)
            profile = UserProfile.objects.get(user=user)
            f.company = profile
            location = request.POST.get('city') + ", " + request.POST.get('state')
            f.location = location
            f.save()

            posted = True

        else:
            print (form.errors)
    else:
        form = CreateJobForm()
    return render(request,'snatch/add_job.html',{'form':form,'posted':posted,'states':states})

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


#Return list of states
def getStates():
    states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut',
            'Delaware', 'Florida', 'Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa',
            'Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan',
            'Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire',
            'New Jersey','New Mexico','New York','North Carolina', 'North Dakota','Ohio','Oklahoma',
            'Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas',
            'Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin', 'Wyoming']
    return states

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
@login_required
def sendRef(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        fname = user.first_name
        lname = user.last_name
        name = fname + lname
        email = request.POST.get('email')
        message = "User "+ name + " has requested a referral!"
        send_email(email, message)

    return render(request, 'snatch/changePassword/send_Referral.html')

@login_required
def get_suggested(request,job_id):
    job = Job.objects.get(id=job_id)
    users = job.applied.all()
    cult = job.culture
    d = defaultdict(list)
    for u in users:
        count = get_difference(u.culture,cult)
        if(count < 2):
            d[count].append(u)
    print d
def get_difference(a,b):
    s = set(b)
    temp3 = [x for x in a if x not in s]
    return len(temp3)
    #send an email to the user
def send_email(email,message):
    server = SMTP("smtp.gmail.com",587) #gmail server
    server.starttls() #connect to server
    server.login('snatchtest1@gmail.com','password12345!')  #login to server
    try:
        server.sendmail('Snatch',email,message) # send message
    finally:
        server.close() #disconnect from server
