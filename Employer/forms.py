from django import forms
from django.contrib.auth.models import User
from Accounts.models import User_type
from Accounts.sample import new_edu_details_1,new_job_categories_1,new_courses_1,new_city_1,new_state_1
from .models import Jobseeker_basic,Job_post_activity,Job_post_skill_set,Job_post,Employer_basic,Company
from Jobseeker.models import Skill_set

class EmployerBasicForm(forms.ModelForm):

    class Meta():
        model = Employer_basic
        fields = ('profile_picture','description')
        help_texts = {
            'profile_picture':None,
            'description': None,
        }
    company_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': "autocomplete"}))
    phone_number = forms.CharField()
    def clean(self):
        all_clean_data=super().clean()
        description = all_clean_data['description']

        if description=="none":
            raise forms.ValidationError("Please enter description")
        #phone number verificaiton
        ph_number = all_clean_data['phone_number'].replace(" ","")
        try:
         ph_number_2 = int(ph_number)
         if ph_number_2 < 1000000000 or ph_number_2 > 9999999999:
             raise forms.ValidationError(" Please Enter a valid phone number")
        except:
            raise forms.ValidationError("Please enter a valid phone number")

class CompanyForm(forms.ModelForm):
    class Meta():
        model = Company
        fields = ('company_logo','company_description')
        help_texts = {
            'company_logo':None,
            'description':None,
        }

    def clean(self):
        all_clean_data = super().clean()

class JobPostForm(forms.ModelForm):

    class Meta():
        model = Job_post
        fields = ('is_company_name_hidden','job_title','job_description','is_work_from_home','min_salary','max_salary','min_experience')
        help_texts = {
            'is_company_name_hidden':None,
            'job_title': None,
            'job_description':None,
            'is_work_from_home':None,
            'min_salary':None,
            'max_salary':None,
            'min_experience':None,
        }
    job_type_name = forms.ChoiceField(choices=new_job_categories_1 ,widget=forms.Select)
    job_length = forms.ChoiceField(choices=(('Not Selected', 'Not Selected'), ('Internship', 'Internship'), ('Full Time', 'Full Time'),('Contract Based', 'Contract Based')),widget=forms.Select)
    city = forms.ChoiceField(choices=new_city_1,widget=forms.Select)

    def clean(self):
        all_clean_data=super().clean()

        job_type_name = all_clean_data['job_type_name']
        if job_type_name == "Not Selected":
            raise forms.ValidationError("Please Select Functional Area")
        city = all_clean_data['city']
        if city == "Not Selected":
            raise forms.ValidationError("Please Select City")
        job_length = all_clean_data['job_length']
        if job_length=="Not Selected":
            raise forms.ValidationError("Please Select Job Type")
        min_salary = all_clean_data['min_salary']
        max_salary = all_clean_data['max_salary']
        min_experience = all_clean_data['min_experience']
        if min_salary < 0:
            raise forms.ValidationError("Please enter valid minimum salary")
        if max_salary < 0:
            raise forms.ValidationError("Please enter valid maximum salary")
        if max_salary< min_salary:
            raise forms.ValidationError("Max salary cannot be less than Min salary")
        if min_experience <0 or min_experience >30:
            raise forms.ValidationError("Please enter valid minimum experience")

class JobPostSkillSetForm(forms.Form):
    skill_set_name = forms.CharField(max_length=30)
    def clean(self):
        all_clean_data=super().clean()


