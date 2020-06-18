from django.shortcuts import render
from .models import Jobseeker_basic,Jobseeker_education,Jobseeker_experience,Jobseeker_skill_set,Skill_set
from Accounts.models import User_type
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import JobseekerBasicForm,JobseekerEducationForm
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.
def jobseeker_home(request):
    user_type_user = User_type.objects.get(user=request.user)
    jobseeker_basic_object,created = Jobseeker_basic.objects.get_or_create(user=user_type_user)
    need_update = 0 #this is for update profile notification
    if created or jobseeker_basic_object.highest_education == 'none' or jobseeker_basic_object.job_type_name == 'none':
        need_update = 1
    return render(request,'Jobseeker/jobseeker_index.html',{'jobseeker_basic':jobseeker_basic_object,'user_type':user_type_user,'need_update':need_update})

def jobseeker_profile(request):
    #User_type Table Object
    user_type_user = User_type.objects.get(user=request.user)
    #Jobseeker_basic Table Object
    jobseeker_basic_object,created = Jobseeker_basic.objects.get_or_create(user=user_type_user)
    need_update = 0 #this is for update profile notification
    if created or jobseeker_basic_object.highest_education == 'none' or jobseeker_basic_object.job_type_name == 'none':
        need_update = 1
    #Jobseeker Educational details
    jobseeker_education_objects = Jobseeker_education.objects.filter(user=jobseeker_basic_object)

    return render(request,'Jobseeker/jobseeker_display_profile.html',{'jobseeker_basic':jobseeker_basic_object,'user_type':user_type_user,'need_update':need_update,'jobseeker_education_objects':jobseeker_education_objects})

def jobseeker_update_profile_basic(request):
    #User_type Table Object
    user_type_user = User_type.objects.get(user=request.user)
    #Jobseeker_basic Table Object
    jobseeker_basic_object,created = Jobseeker_basic.objects.get_or_create(user=user_type_user)
    need_update = 0 #this is for update profile notification
    if created or jobseeker_basic_object.highest_education == 'none' or jobseeker_basic_object.job_type_name == 'none':
        need_update = 1
     #Logic starts here
    if request.method=="POST":
        basic_form=JobseekerBasicForm(request.POST,request.FILES)
        if basic_form.is_valid():
            print('form is valid \n')
            formInstance = basic_form.save(commit=False)
            formInstance.user = user_type_user
            formInstance.highest_education = request.POST.get('highest_education')
            formInstance.job_type_name = request.POST.get('job_type_name')
            formInstance.save()
            user_type_user.phone_number = request.POST.get('phone_number')
            user_type_user.save()
            print('\nsaved successfully')
            return redirect(reverse('Jobseeker:jobseeker_profile'))

    else:
        basic_form = JobseekerBasicForm()
    return render(request,'Jobseeker/jobseeker_update_profile_basic.html',{'jobseeker_basic':jobseeker_basic_object,'user_type':user_type_user,'need_update':0,'basic_form':basic_form})


def jobseeker_update_education(request):
    # User_type Table Object
    user_type_user = User_type.objects.get(user=request.user)
    # Jobseeker_basic Table Object
    jobseeker_basic_object, created = Jobseeker_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or jobseeker_basic_object.highest_education == 'none' or jobseeker_basic_object.job_type_name == 'none':
        need_update = 1
    # Logic starts here
    if request.method == "POST":
        education_form = JobseekerEducationForm(data=request.POST)
        if education_form.is_valid():
            print('form is valid \n')
            formInstance = education_form.save(commit=False)
            formInstance.user = jobseeker_basic_object
            formInstance.degree_type = request.POST.get('degree_type')
            formInstance.degree_name = request.POST.get('degree_name')
            formInstance.save()
            return redirect(reverse('Jobseeker:jobseeker_profile'))
    else:
        education_form = JobseekerEducationForm()
    return render(request,'Jobseeker/jobseeker_update_education.html',{'jobseeker_basic': jobseeker_basic_object, 'user_type': user_type_user, 'need_update': 0,'education_form': education_form})


def jobseeker_update_education_crud(request,operation,id):
    print('The operation is '+operation+"  and id is "+str(id))
    if operation=='new':
        return redirect(reverse('Jobseeker:jobseeker_update_education'))
    elif operation == 'delete':
        target_object = Jobseeker_education.objects.get(pk=id)
        target_object.delete()
        print('\ndeleted successfully\n')
        return redirect(reverse('Jobseeker:jobseeker_profile'))
    else:
        return redirect(reverse('Jobseeker:jobseeker_update_education'))