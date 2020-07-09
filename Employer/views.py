from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponse
from Accounts.models import User_type
from Jobseeker.models import *
from django.contrib.auth.models import User
from .models import Employer_basic, Job_post, Job_post_skill_set, Job_post_activity, Jobseeker_basic, Announcement, \
    Company
from .forms import EmployerBasicForm, CompanyForm, JobPostForm,JobPostSkillSetForm
from django.shortcuts import redirect
from django.urls import reverse
#for paginator
from django.core.paginator import Paginator

# Create your views here.
def employer_home(request):
    user_type_user = User_type.objects.get(user=request.user)
    employer_basic_object, created = Employer_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or employer_basic_object.description == 'none':
        need_update = 1
    return render(request, 'Employer/employer_index.html',
                  {'user_type': user_type_user, 'employer_basic': employer_basic_object, 'need_update': need_update})


def employer_profile(request):
    user_type_user = User_type.objects.get(user=request.user)
    employer_basic_object, created = Employer_basic.objects.get_or_create(user=user_type_user)

    need_update = 0  # this is for update profile notification
    if created or employer_basic_object.description == 'none':
        need_update = 1
    return render(request, 'Employer/employer_display_profile.html',
                  {'user_type': user_type_user, 'employer_basic': employer_basic_object, 'need_update': need_update})


def employer_update_profile_basic(request):
    user_type_user = User_type.objects.get(user=request.user)
    employer_basic_object, created = Employer_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or employer_basic_object.description == 'none':
        need_update = 1
    # Company names list
    company_names = []
    all_company_objects = Company.objects.all()
    for company_object in all_company_objects:
        company_names.append(company_object.company_name)

    # Logic starts here
    if request.method == "POST":
        basic_form = EmployerBasicForm(request.POST, request.FILES)
        if basic_form.is_valid():

            employer_basic_object.profile_picture = basic_form.cleaned_data['profile_picture']
            employer_basic_object.description = basic_form.cleaned_data['description']
            # checking if he owner of company or just an employer of the company
            company_name_given = basic_form.cleaned_data['company_name']
            print("Company name is : " + company_name_given)

            if company_name_given in company_names:
                if employer_basic_object.company is not None:
                    if employer_basic_object.is_owner == False:
                        employer_basic_object.company = Company.objects.get(company_name=company_name_given)
                        employer_basic_object.is_owner = False
                    elif employer_basic_object.is_owner == True:
                        if company_name_given != employer_basic_object.company.company_name:
                            company_to_be_deleted = Company.objects.get(
                                company_name=employer_basic_object.company.company_name)
                            company_to_be_deleted.delete()
                            employer_basic_object.is_owner = False
                        employer_basic_object.company = Company.objects.get(company_name=company_name_given)
                else:
                    employer_basic_object.company = Company.objects.get(company_name=company_name_given)
                    employer_basic_object.is_owner = False
            elif company_name_given != "":
                if employer_basic_object.is_owner == False:
                    new_company_object = Company.objects.create(company_name=company_name_given)
                    employer_basic_object.is_owner = True
                    employer_basic_object.company = new_company_object
                elif employer_basic_object.is_owner == True:
                    company_to_be_deleted = Company.objects.get(company_name=employer_basic_object.company.company_name)
                    company_to_be_deleted.delete()
                    new_company_object = Company.objects.create(company_name=company_name_given)
                    employer_basic_object.is_owner = True
                    employer_basic_object.company = new_company_object
            else:
                if employer_basic_object.is_owner == False:
                    employer_basic_object.company = None
                    employer_basic_object.is_owner = False
                else:
                    company_to_be_deleted = Company.objects.get(company_name=employer_basic_object.company.company_name)
                    company_to_be_deleted.delete()
                    employer_basic_object.company = None
                    employer_basic_object.is_owner = False
            employer_basic_object.save()

            # phone number verification
            try:
                ph_object = User_type.objects.get(phone_number=request.POST.get('phone_number').replace(" ", ""))
                if ph_object.user != request.user:
                    messages.error(request, "A user with that phone number already exists")
                    return redirect(reverse('Employer:employer_update_profile_basic'))
                else:
                    user_type_user.phone_number = request.POST.get('phone_number')
            except ObjectDoesNotExist:
                user_type_user.phone_number = request.POST.get('phone_number')
            user_type_user.save()
            print('\nsaved successfully')
            return redirect(reverse('Employer:employer_profile'))

    else:
        if employer_basic_object.company is not None:
            print('Im sending company name also')
            my_dict = {'phone_number': user_type_user.phone_number, 'description': employer_basic_object.description,
                       'company_name': employer_basic_object.company.company_name}
            basic_form = EmployerBasicForm(initial=my_dict)
        else:
            print('Im NOT Sending company name')
            my_dict = {'phone_number': user_type_user.phone_number, 'description': employer_basic_object.description}
            basic_form = EmployerBasicForm(initial=my_dict)
    return render(request, 'Employer/employer_update_profile_basic.html',
                  {'employer_basic': employer_basic_object, 'user_type': user_type_user, 'need_update': 0,
                   'basic_form': basic_form, 'company_names': company_names})


def edit_company(request, company_name):
    user_type_user = User_type.objects.get(user=request.user)
    employer_basic_object, created = Employer_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or employer_basic_object.description == 'none':
        need_update = 1
    print('COMPANY name is ' + company_name)
    company_object = Company.objects.get(company_name=company_name)
    if request.method == "POST":
        print('IM in POST If condition')
        basic_form = CompanyForm(request.POST, request.FILES)
        if basic_form.is_valid():
            company_object.company_logo = basic_form.cleaned_data['company_logo']
            company_object.company_description = basic_form.cleaned_data['company_description']
            company_object.save()
            return redirect(reverse('Employer:employer_profile'))
    else:
        print("Im in ELSE if condition")
        my_dict = {'company_description': company_object.company_description}
        basic_form = CompanyForm(initial=my_dict)
        return render(request, 'Employer/edit_company.html',
                      {'need_update': 0, 'basic_form': basic_form, 'company_name': company_name})


def employer_post_job(request, id):
    user_type_user = User_type.objects.get(user=request.user)
    employer_basic_object, created = Employer_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or employer_basic_object.description == 'none':
        need_update = 1
    job_post_form = JobPostForm()
    # Logic starts here
    if id > 0:
        target_object = Job_post.objects.get(pk=id)
    if request.method == "POST":
        if id == 0:
            job_post_form = JobPostForm(data=request.POST)
            if job_post_form.is_valid():
                print(' Hi Job Post Form is valid \n')
                formInstance = job_post_form.save(commit=False)
                formInstance.posted_by_id = employer_basic_object
                formInstance.job_type_name = request.POST.get('job_type_name')
                formInstance.job_length = request.POST.get('job_length')
                formInstance.city = request.POST.get('city')
                formInstance.save()
                return redirect(reverse('Employer:employer_view_jobs'))
        else:
            job_post_form = JobPostForm(data=request.POST)
            if job_post_form.is_valid():
                target_object = Job_post.objects.get(pk=id)
                target_object.job_type_name = request.POST.get('job_type_name')
                target_object.job_length = request.POST.get('job_length')
                target_object.city = request.POST.get('city')
                target_object.is_company_name_hidden = request.POST.get('is_company_name_hidden')=='on'
                target_object.job_title = request.POST.get('job_title')
                target_object.job_description = request.POST.get('job_description')
                target_object.min_salary = request.POST.get('min_salary')
                target_object.max_salary = request.POST.get('max_salary')
                target_object.min_experience = request.POST.get('min_experience')
                target_object.is_work_from_home = request.POST.get('is_work_from_home')=='on'
                target_object.save()
                return redirect(reverse('Employer:employer_view_jobs'))

    else:
        if id == 0:
            job_post_form = JobPostForm()
        else:
            my_dict = {'job_type_name': target_object.job_type_name, 'job_length': target_object.job_length,
                       'city': target_object.city, 'is_company_name_hidden': target_object.is_company_name_hidden,
                       'job_title': target_object.job_title, 'job_description': target_object.job_description,
                       'min_salary': target_object.min_salary, 'max_salary': target_object.max_salary,
                       'min_experience': target_object.min_experience,
                       'is_work_from_home': target_object.is_work_from_home}
            job_post_form = JobPostForm(initial=my_dict)
    return render(request, 'Employer/employer_post_job.html',
                  {'employer_basic': employer_basic_object, 'user_type': user_type_user, 'need_update': 0,
                   'job_post_form': job_post_form, 'id': id})

def employer_post_job_crud(request, operation, id):
    print('The operation is ' + operation + "  and id is " + str(id))
    if operation == 'new':
        return employer_post_job(request, 0)
    elif operation == 'delete':
        target_object = Job_post.objects.get(pk=id)
        target_object.delete()
        print('\ndeleted successfully\n')
        return redirect(reverse('Employer:employer_view_jobs'))
    elif operation == 'edit':
        return employer_post_job(request, id)

def employer_view_jobs(request):
    user_type_user = User_type.objects.get(user=request.user)
    employer_basic_object, created = Employer_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or employer_basic_object.description == 'none':
        need_update = 1
    job_post_objects = Job_post.objects.filter(posted_by_id=employer_basic_object)
    job_post_skills_objects_array = []
    for job_post_object in job_post_objects:
        job_post_skills_objects_array.append(Job_post_skill_set.objects.filter(job_post_id=job_post_object))
    skills_array_individual =[]
    total_job_post_skills_array =[]
    for queryset in job_post_skills_objects_array:
        if queryset.count()>0:
            for item in queryset:
                skills_array_individual.append(item.skill_set_id.skill_set_name)
        total_job_post_skills_array.append(skills_array_individual)
        skills_array_individual=[]
    final_dict ={}
    for object,skills in zip(job_post_objects,total_job_post_skills_array):
        final_dict[object]=skills
    final_dict_touple = final_dict.items()
    final_list = list(final_dict_touple)

    #logic for paginator starts here
    paginator = Paginator(final_list,5)
    page = request.GET.get('page')
    final_list = paginator.get_page(page)
    return render(request,'Employer/employer_view_jobs.html',{'user_type': user_type_user, 'employer_basic': employer_basic_object, 'need_update': need_update,'final_list':final_list,'paginator':paginator})

def toggle_job_post_activity(request,id):
    job_post_object = Job_post.objects.get(pk=id)
    if job_post_object.is_active:
        print('hello there')
        job_post_object.is_active = False
        job_post_object.save()
    else:
        job_post_object.is_active = True
        job_post_object.save()
    return redirect(reverse('Employer:employer_view_jobs'))

def employer_view_job(request,id):
    user_type_user = User_type.objects.get(user=request.user)
    employer_basic_object, created = Employer_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or employer_basic_object.description == 'none':
        need_update = 1
    job_post_object = Job_post.objects.get(pk=id)
    job_post_skill_set_objects = Job_post_skill_set.objects.filter(job_post_id=job_post_object)
    skill_set_array =[]
    if job_post_skill_set_objects.count()>0:
        for object in job_post_skill_set_objects:
            skill_set_array.append(object.skill_set_id.skill_set_name)
    job_post = (job_post_object,skill_set_array)
    desc_list = job_post_object.job_description.split(".")
    return render(request,'Employer/employer_view_job.html',{'user_type': user_type_user, 'employer_basic': employer_basic_object, 'need_update': need_update,'job_post':job_post,'desc_list':desc_list})

def job_post_update_skill_set(request,operation,id,name):
    user_type_user = User_type.objects.get(user=request.user)
    employer_basic_object,created= Employer_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or employer_basic_object.description == 'none':
        need_update = 1
    #skill set objects skill array containing all the skill set names as list items used in the autocomplete javascript function
    skill_set_objects = Skill_set.objects.all()
    skills = []
    for skill in skill_set_objects:
        skills.append(skill.skill_set_name)
    job_post_object = Job_post.objects.get(pk=id)
    if request.method == "POST":
        print('hello im in POST')
        skill_set_form = JobPostSkillSetForm(data=request.POST)
        if skill_set_form.is_valid():
            print('Skill set form is valid \n')
            skill_set_name = request.POST.get('skill_set_name')
            skill_set_object, created = Skill_set.objects.get_or_create(defaults={'skill_set_name': skill_set_name},skill_set_name__iexact=skill_set_name)
            redundant_objects =Job_post_skill_set.objects.filter(job_post_id=job_post_object,skill_set_id=skill_set_object)
            if redundant_objects.count() > 0:
                messages.error(request, "Skill already exists")
                return redirect(reverse('Employer:job_post_update_skill_set', kwargs={'operation':operation,'id':id,'name':name}))
            new_object = Job_post_skill_set.objects.create(job_post_id=job_post_object,skill_set_id=skill_set_object)
            new_object.save()
            return redirect(reverse('Employer:employer_view_job',kwargs={'id':id}))
    if operation == 'delete':
        target_skill_set_object = Skill_set.objects.get(skill_set_name=name)
        job_post_skill_set_object = Job_post_skill_set.objects.filter(job_post_id=job_post_object).filter(skill_set_id=target_skill_set_object).first()
        job_post_skill_set_object.delete()
        return redirect(reverse('Employer:employer_view_job',kwargs={'id':id}))
    elif operation == 'new':
        skill_set_form = JobPostSkillSetForm
        return render(request,'Employer/job_post_update_skill_set.html',{'user_type': user_type_user, 'employer_basic': employer_basic_object, 'need_update': need_update,'operation':operation,'id':id,'name':name,'skills':skills,'skill_set_form':skill_set_form})

def job_post_view_applications(request,id):
    user_type_user = User_type.objects.get(user=request.user)
    employer_basic_object,created= Employer_basic.objects.get_or_create(user=user_type_user)
    need_update = 0  # this is for update profile notification
    if created or employer_basic_object.description == 'none':
        need_update = 1
    job_post_object = Job_post.objects.get(pk=id)
    job_post_activity_objects = Job_post_activity.objects.filter(job_post_id=job_post_object).order_by('-pk')
    #logic for paginator starts here
    paginator = Paginator(job_post_activity_objects,9)
    page = request.GET.get('page')
    job_post_activity_objects = paginator.get_page(page)
    return render(request,'Employer/job_post_view_applications.html',{'user_type': user_type_user, 'employer_basic': employer_basic_object, 'need_update': need_update,'applications':job_post_activity_objects,'paginator':paginator})

def job_post_view_applications_full_profile(request,username):
    #User_type Table Object
    user_object = User.objects.get(username=username)
    user_type_user = User_type.objects.get(user=user_object)
    #Jobseeker_basic Table Object
    jobseeker_basic_object = Jobseeker_basic.objects.get(user=user_type_user)
    #Jobseeker Educational details
    jobseeker_education_objects = Jobseeker_education.objects.filter(user=jobseeker_basic_object)
    #Jobseeker Work Experience Details
    jobseeker_experience_objects = Jobseeker_experience.objects.filter(user=jobseeker_basic_object)
    #Jobseeker Skillset details
    jobseeker_skill_set_objects = Jobseeker_skill_set.objects.filter(user=jobseeker_basic_object)
    #Skillset objects
    skill_set_objects = Skill_set.objects.all()
    return render(request,'Employer/job_post_view_applications_full_profile.html',{'jobseeker_basic':jobseeker_basic_object,'user_type':user_type_user,'jobseeker_education_objects':jobseeker_education_objects,'jobseeker_experience_objects':jobseeker_experience_objects,'jobseeker_skill_set_objects':jobseeker_skill_set_objects,'skill_set_objects':skill_set_objects})

