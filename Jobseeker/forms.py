from django import forms
from django.contrib.auth.models import User
from Accounts.models import User_type
from Jobseeker.models import Jobseeker_basic,Jobseeker_skill_set,Jobseeker_experience,Jobseeker_education,Skill_set
from Accounts.sample import new_edu_details_1,new_job_categories_1,new_courses_1

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

        if User_type.objects.filter(phone_number=ph_number).exists():
            raise forms.ValidationError("A user with the phone number already exists")


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

