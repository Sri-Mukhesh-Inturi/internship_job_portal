from django import forms
from django.contrib.auth.models import User
from Accounts.models import User_type
from Jobseeker.models import Jobseeker_basic,Jobseeker_skill_set,Jobseeker_experience,Jobseeker_education,Skill_set
from Accounts.sample import new_edu_details_1,new_job_categories_1,new_courses_1,new_city_1

class JobseekerBasicForm(forms.ModelForm):

    class Meta():
        model = Jobseeker_basic
        fields = ('profile_picture','salary_expectation','description','resume')
        help_texts = {
            'profile_picture':None,
            'salary_expectation':None,
            'description': None,
            'resume':None,
        }
    highest_education = forms.ChoiceField(choices=new_edu_details_1,widget=forms.Select)
    job_type_name = forms.ChoiceField(choices=new_job_categories_1 ,widget=forms.Select)
    phone_number = forms.CharField()
    def clean(self):
        all_clean_data=super().clean()
        salary = all_clean_data['salary_expectation']
        edu = all_clean_data['highest_education']
        profession = all_clean_data['job_type_name']
        #salary verification
        if salary < 0:
            raise forms.ValidationError("Salary Expectation Cannot Be less than 0")
        elif profession == 'Not Selected':
            raise forms.ValidationError("Please Choose Profession")
        elif edu =='Not Selected':
            raise forms.ValidationError("Please Choose Education")
        #phone number verificaiton
        ph_number = all_clean_data['phone_number'].replace(" ","")
        try:
         ph_number_2 = int(ph_number)
         if ph_number_2 < 1000000000 or ph_number_2 > 9999999999:
             raise forms.ValidationError(" Please Enter a valid phone number")
        except:
            raise forms.ValidationError("Please enter a valid phone number")
        #phone number checking from existing users


class JobseekerEducationForm(forms.ModelForm):

    class Meta():
        model = Jobseeker_education
        fields = ('institute','start_date','end_date','cgpa')
        help_texts = {
            'institute': None,
            'start_date':None,
            'end_date': None,
            'cgpa': None,
        }
        widgets={
                   "start_date":forms.DateInput(format=('%d-%m-%Y'),attrs={'type':'date'}),
                   "end_date":forms.DateInput(format=('%d-%m-%Y'),attrs={'type':'date'}),
                }
    degree_type = forms.ChoiceField(choices=new_edu_details_1,widget=forms.Select)
    degree_name = forms.ChoiceField(choices=new_courses_1,widget=forms.Select)
    def clean(self):
        all_clean_data=super().clean()
        degree_type = all_clean_data['degree_type']
        degree_name = all_clean_data['degree_name']
        cgpa = all_clean_data['cgpa']
        start_date = all_clean_data['start_date']
        end_date = all_clean_data['end_date']
        if degree_type == 'Not Selected':
            raise forms.ValidationError("Please Choose Degree Type")
        if degree_name =='Not Selected':
            raise forms.ValidationError("Please Choose Degree Name")
        if cgpa > 10:
            raise forms.ValidationError("CGPA cant be more than 10")
        elif cgpa < 0:
            raise forms.ValidationError("CGPA cant be less than 0")
        if start_date > end_date:
            raise forms.ValidationError("end date can't be before start date")


class JobseekerExperienceForm(forms.ModelForm):

    class Meta():
        model = Jobseeker_experience
        fields = ('job_title','company_name','start_date','end_date','job_description')
        help_texts = {
            'job_title': None,
            'company_name':None,
            'start_date':None,
            'end_date': None,
            'job_description': None,
        }
        widgets={
                   "start_date":forms.DateInput(format=('%d-%m-%Y'),attrs={'type':'date'}),
                   "end_date":forms.DateInput(format=('%d-%m-%Y'),attrs={'type':'date'}),
                }
    job_type = forms.ChoiceField(choices=(('Not Selected','Not Selected'),('Internship','Internship'),('Full Time','Full Time')),widget=forms.Select)
    job_location_city = forms.ChoiceField(choices=new_city_1, widget=forms.Select)
    def clean(self):
        all_clean_data=super().clean()
        start_date = all_clean_data['start_date']
        end_date = all_clean_data['end_date']
        job_type = all_clean_data['job_type']
        if job_type=='Not Selected':
            raise forms.ValidationError("Please select Job Type")
        if start_date > end_date:
            raise forms.ValidationError("end date can't be before start date")

class JobseekerSkillSetForm(forms.ModelForm):

    class Meta():
        model = Jobseeker_skill_set
        fields = ('skill_level',)
        help_texts = {
            'skill_level': None,
        }
    skill_set_name = forms.CharField(max_length=30)
    def clean(self):
        all_clean_data=super().clean()
        skill_level = all_clean_data['skill_level']
        if skill_level <0 or skill_level>10:
            raise forms.ValidationError("Invalid Skill Level")

