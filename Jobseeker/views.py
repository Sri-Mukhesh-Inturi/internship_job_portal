from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import Jobseeker_basic,Jobseeker_education,Jobseeker_experience,Jobseeker_skill_set,Skill_set
from Accounts.models import User_type
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import JobseekerBasicForm,JobseekerEducationForm,JobseekerExperienceForm,JobseekerSkillSetForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


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
    #Jobseeker Work Experience Details
    jobseeker_experience_objects = Jobseeker_experience.objects.filter(user=jobseeker_basic_object)
    #Jobseeker Skillset details
    jobseeker_skill_set_objects = Jobseeker_skill_set.objects.filter(user=jobseeker_basic_object)
    #Skillset objects
    skill_set_objects = Skill_set.objects.all()
    return render(request,'Jobseeker/jobseeker_display_profile.html',{'jobseeker_basic':jobseeker_basic_object,'user_type':user_type_user,'need_update':need_update,'jobseeker_education_objects':jobseeker_education_objects,'jobseeker_experience_objects':jobseeker_experience_objects,'jobseeker_skill_set_objects':jobseeker_skill_set_objects,'skill_set_objects':skill_set_objects})

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
            jobseeker_basic_object.profile_picture = basic_form.cleaned_data['profile_picture']
            jobseeker_basic_object.salary_expectation =basic_form.cleaned_data['salary_expectation']
            jobseeker_basic_object.description = basic_form.cleaned_data['description']
            jobseeker_basic_object.highest_education = basic_form.cleaned_data['highest_education']
            jobseeker_basic_object.resume = basic_form.cleaned_data['resume']
            jobseeker_basic_object.job_type_name = basic_form.cleaned_data['job_type_name']
            jobseeker_basic_object.save()

            # formInstance = basic_form.save(commit=False)
            # formInstance.user = user_type_user
            # formInstance.highest_education = request.POST.get('highest_education')
            # formInstance.job_type_name = request.POST.get('job_type_name')
            # formInstance.save()
            #phone number verification
            try:
                ph_object = User_type.objects.get(phone_number=request.POST.get('phone_number').replace(" ",""))
                if ph_object.user != request.user:
                    messages.error(request, "A user with that phone number already exists")
                    return redirect(reverse('Jobseeker:jobseeker_update_profile_basic'))
                else:
                    user_type_user.phone_number = request.POST.get('phone_number')
            except ObjectDoesNotExist:
                user_type_user.phone_number = request.POST.get('phone_number')
            user_type_user.save()
            print('\nsaved successfully')
            return redirect(reverse('Jobseeker:jobseeker_profile'))

    else:
        if created==True:
            my_dict ={'phone_number':user_type_user.phone_number}
            basic_form = JobseekerBasicForm(initial=my_dict)
        else:
            my_dict = {
                           'salary_expectation': jobseeker_basic_object.salary_expectation,
                           'description': jobseeker_basic_object.description,
                           'highest_education': jobseeker_basic_object.highest_education,
                           'job_type_name': jobseeker_basic_object.job_type_name,
                           'phone_number': user_type_user.phone_number}

            basic_form = JobseekerBasicForm(initial=my_dict)
    return render(request,'Jobseeker/jobseeker_update_profile_basic.html',{'jobseeker_basic':jobseeker_basic_object,'user_type':user_type_user,'need_update':0,'basic_form':basic_form,'id':id})



def jobseeker_update_education(request,id):
    # User_type Table Object
    user_type_user = User_type.objects.get(user=request.user)
    # Jobseeker_basic Table Object
    jobseeker_basic_object, created = Jobseeker_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or jobseeker_basic_object.highest_education == 'none' or jobseeker_basic_object.job_type_name == 'none':
        need_update = 1
    # Logic starts here
    if id>0:
        target_object = Jobseeker_education.objects.get(pk=id)
    if request.method == "POST":
        if id==0:
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
            education_form = JobseekerEducationForm(data=request.POST)
            if education_form.is_valid():
                target_object = Jobseeker_education.objects.get(pk=id)
                target_object.degree_type=request.POST.get('degree_type')
                target_object.degree_name = request.POST.get('degree_name')
                target_object.cgpa = request.POST.get('cgpa')
                target_object.start_date = request.POST.get('start_date')
                target_object.end_date = request.POST.get('end_date')
                target_object.institute = request.POST.get('institute')
                target_object.save()
                return redirect(reverse('Jobseeker:jobseeker_profile'))

    else:
        if id==0:
            education_form = JobseekerEducationForm()
        else:
            my_dict = {'degree_type':target_object.degree_type,'degree_name':target_object.degree_name,'institute':target_object.institute,'cgpa':target_object.cgpa,'start_date':target_object.start_date,'end_date':target_object.end_date}
            education_form = JobseekerEducationForm(initial=my_dict)
    return render(request,'Jobseeker/jobseeker_update_education.html',{'jobseeker_basic': jobseeker_basic_object, 'user_type': user_type_user, 'need_update': 0,'education_form': education_form,'id':id})


def jobseeker_update_education_crud(request,operation,id):
    print('The operation is '+operation+"  and id is "+str(id))
    if operation=='new':
        return jobseeker_update_education(request,0)
    elif operation == 'delete':
        target_object = Jobseeker_education.objects.get(pk=id)
        target_object.delete()
        print('\ndeleted successfully\n')
        return redirect(reverse('Jobseeker:jobseeker_profile'))
    elif operation=='edit':
        return jobseeker_update_education(request,id)

    #for JOBSEEKER EXPERIENCE


def jobseeker_update_experience(request, id):
    # User_type Table Object
    user_type_user = User_type.objects.get(user=request.user)
    # Jobseeker_basic Table Object
    jobseeker_basic_object, created = Jobseeker_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or jobseeker_basic_object.highest_education == 'none' or jobseeker_basic_object.job_type_name == 'none':
        need_update = 1
    # Logic starts here
    if id > 0:
        target_object = Jobseeker_experience.objects.get(pk=id)
    if request.method == "POST":
        if id == 0:
            experience_form = JobseekerExperienceForm(data=request.POST)
            if experience_form.is_valid():
                print('form is valid \n')
                formInstance = experience_form.save(commit=False)
                formInstance.user = jobseeker_basic_object
                formInstance.job_location_city = request.POST.get('job_location_city')
                formInstance.job_type = request.POST.get('job_type')
                formInstance.save()
                return redirect(reverse('Jobseeker:jobseeker_profile'))
        else:
            experience_form = JobseekerExperienceForm(data=request.POST)
            if experience_form.is_valid():
                target_object = Jobseeker_experience.objects.get(pk=id)
                target_object.job_location_city = request.POST.get('job_location_city')
                target_object.job_title = request.POST.get('job_title')
                target_object.job_description = request.POST.get('job_description')
                target_object.start_date = request.POST.get('start_date')
                target_object.end_date = request.POST.get('end_date')
                target_object.company_name = request.POST.get('company_name')
                target_object.job_type = request.POST.get('job_type')
                target_object.save()
                return redirect(reverse('Jobseeker:jobseeker_profile'))

    else:
        if id == 0:
            experience_form = JobseekerExperienceForm()
        else:
            my_dict = {'job_type':target_object.job_type,'job_location_city': target_object.job_location_city, 'job_title': target_object.job_title,
                       'job_description': target_object.job_description, 'company_name': target_object.company_name,
                       'start_date': target_object.start_date, 'end_date': target_object.end_date}
            experience_form = JobseekerExperienceForm(initial=my_dict)
    return render(request, 'Jobseeker/jobseeker_update_experience.html',
                  {'jobseeker_basic': jobseeker_basic_object, 'user_type': user_type_user, 'need_update': 0,
                   'experience_form': experience_form, 'id': id})


def jobseeker_update_experience_crud(request, operation, id):
    print('The operation is ' + operation + "  and id is " + str(id))
    if operation == 'new':
        return jobseeker_update_experience(request, 0)
    elif operation == 'delete':
        target_object = Jobseeker_experience.objects.get(pk=id)
        target_object.delete()
        print('\ndeleted successfully\n')
        return redirect(reverse('Jobseeker:jobseeker_profile'))
    elif operation == 'edit':
        return jobseeker_update_experience(request, id)
#JOBSEEKER SKILL SET
def jobseeker_update_skill_set(request, id):
    # User_type Table Object
    user_type_user = User_type.objects.get(user=request.user)
    # Jobseeker_basic Table Object
    jobseeker_basic_object, created = Jobseeker_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or jobseeker_basic_object.highest_education == 'none' or jobseeker_basic_object.job_type_name == 'none':
        need_update = 1
    # Logic starts here
    if id > 0:
        target_object = Jobseeker_skill_set.objects.get(pk=id)
    if request.method == "POST":
        if id == 0:
            skill_set_form = JobseekerSkillSetForm(data=request.POST)
            if skill_set_form.is_valid():
                print('form is valid \n')
                skill_set_name = request.POST.get('skill_set_name')
                formInstance = skill_set_form.save(commit=False)
                formInstance.user = jobseeker_basic_object
                skill_set_object,created = Skill_set.objects.get_or_create(defaults={'skill_set_name':skill_set_name}, skill_set_name__iexact=skill_set_name)
                formInstance.skill_set_id=skill_set_object
                formInstance.save()
                return redirect(reverse('Jobseeker:jobseeker_profile'))
    else:
        if id == 0:
            skill_set_form = JobseekerSkillSetForm()
    return render(request, 'Jobseeker/jobseeker_update_skill_set.html',
                  {'jobseeker_basic': jobseeker_basic_object, 'user_type': user_type_user, 'need_update': 0,
                   'skill_set_form': skill_set_form, 'id': id})


def jobseeker_update_skill_set_crud(request, operation, id):
    print('The operation is ' + operation + "  and id is " + str(id))
    if operation == 'new':
        return jobseeker_update_skill_set(request, 0)
    elif operation == 'delete':
        target_object = Jobseeker_skill_set.objects.get(pk=id)
        target_object.delete()
        print('\ndeleted successfully\n')
        return redirect(reverse('Jobseeker:jobseeker_profile'))

