from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponse
from Accounts.models import User_type
from Jobseeker.models import Skill_set
from django.contrib.auth.models import User
from .models import Employer_basic, Job_post, Job_post_skill_set, Job_post_activity, Jobseeker_basic, Announcement, \
    Company
from .forms import EmployerBasicForm, CompanyForm, JobPostForm
from django.shortcuts import redirect
from django.urls import reverse


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
                return redirect(reverse('Employer:employer_profile'))
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
                return redirect(reverse('Employer:employer_profile'))

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
        return redirect(reverse('Employer:employer_profile'))
    elif operation == 'edit':
        return employer_post_job(request, id)
