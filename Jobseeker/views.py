from django.shortcuts import render

# Create your views here.
def jobseeker_home(request):

    return render(request,'Jobseeker/jobseeker_index.html')
