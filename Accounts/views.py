from django.shortcuts import render
from Accounts.models import User_type
from Accounts.forms import UserForm,LoginForm
from django.contrib.auth.models import User
from Employer import views as employer
from Jobseeker import views as jobseeker
# Create your views here.

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django import forms
from django.contrib import messages
from django.shortcuts import redirect

def index(request):
    if request.user.is_authenticated:
        user_type_object,created = User_type.objects.get_or_create(user=request.user)
        if user_type_object.user_type_name == 'jobseeker':
            return redirect(reverse('Jobseeker:jobseeker_home'))
        elif user_type_object.user_type_name == 'employer':
            return redirect(reverse('Employer:employer_home'))
    else:
        return render(request,'Accounts/index.html')

def register(request):
    registered=False
    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password) #hashing the password
            user.save() #save hash password to database
            registered=True
            #create user_type
            user_type_object,created = User_type.objects.get_or_create(user=user)
            user_type_object.user_type_name=request.POST.get('user_type_name')
            user_type_object.current_city = request.POST.get('current_city')
            user_type_object.phone_number = request.POST.get('phone_number').replace(" ","")
            user_type_object.save()
    else:
        user_form=UserForm()
    return render(request,'Accounts/registration.html',{'user_form':user_form,'registered':registered,})

@login_required
def user_logout(request):
    logout(request)
    print(request.user.username + 'has been logged out')
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method=="POST":
        login_form=LoginForm(data=request.POST)
        if login_form.is_valid():
            user_name_or_num = request.POST.get('user_name_or_num')
            password = request.POST.get('password')
            actual_user_name = ""
            if_num = ""
            num = 0
            try:
                if_num = user_name_or_num.replace(" ","")
                num = int(if_num)
                if User_type.objects.filter(phone_number=if_num).exists():
                    actual_user_name = User_type.objects.get(phone_number=if_num).user.username

            except:
                if User.objects.filter(username = user_name_or_num).exists():
                    actual_user_name = User.objects.get(username=user_name_or_num)
            user = authenticate(username=actual_user_name, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    print(request.user.username + ' is logged in successfully')
                    user_type = User_type.objects.get(user = user).user_type_name

                    if user_type == 'jobseeker':
                        return redirect(reverse('Jobseeker:jobseeker_home'))
                        #return render(request,'Accounts/jobseeker_index.html')

                    elif user_type == 'employer':
                        return redirect(reverse('Employer:employer_home'))
                        #return render(request,'Accounts/employer_index.html')
                    # return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse("Login Details are correct but the Account has been disabled")
            else:
                messages.error(request, "Incorrect Password")
                print("someone tried to login and failed")
                print("username:{} and password {}".format(actual_user_name,password))

    else:
        login_form = LoginForm()
    return render(request, 'Accounts/login.html', {'login_form':login_form})