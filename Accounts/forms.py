from django import forms
from django.contrib.auth.models import User
from Accounts.models import User_type
from .sample import new_city_1
from django.core.validators import validate_email
class UserForm(forms.ModelForm):

    class Meta():
        model=User
        fields=('username','first_name','last_name','email','password')
        help_texts = {
            'username': None,
            'email': None,
        }
        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'password': forms.TextInput(),
        }


    password=forms.CharField(widget=forms.PasswordInput())
    retype_password=forms.CharField(widget=forms.PasswordInput())
    user_type_choices=[
        ('employer','employer'),
        ('jobseeker','jobseeker')
    ]
    user_type_name = forms.ChoiceField(choices=user_type_choices,widget=forms.RadioSelect)
    current_city = forms.ChoiceField(choices=new_city_1,widget=forms.Select)
    phone_number = forms.CharField()

    def clean(self):
        all_clean_data=super().clean()
        username=all_clean_data['username']
        city = all_clean_data['current_city']
        if city=='Not Selected':
            raise forms.ValidationError("Please select city")
        #email verification
        try:
            email=all_clean_data['email']
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
        except:
            raise forms.ValidationError("Invalid Email Entered")

        #password verification
        p1 = all_clean_data['password']
        p2 = all_clean_data['retype_password']
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
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


#This is the form for login
class LoginForm(forms.Form):
    user_name_or_num = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    def clean(self):
        all_clean_data = super().clean()
        param_1 = all_clean_data['user_name_or_num']
        password = all_clean_data['password']
        try:
            param_1 = param_1.replace(" ","")
            param_1_new = int(param_1)
            if User_type.objects.filter(phone_number = param_1).exists():
                print("phone number is valid")
            else:
                raise forms.ValidationError("Please Enter Correct Phone Number")
        except:
            if User.objects.filter(username=param_1).exists():
                print("Username is valid")
            else:
                raise forms.ValidationError("Please Enter Correct Username")
