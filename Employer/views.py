from django.shortcuts import render

# Create your views here.
def employer_home(request):
    return render(request,'Employer/employer_index.html')
