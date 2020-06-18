import os
module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, '../static/text/cities.txt')
file_path_to_educational_details = os.path.join(module_dir, '../static/text/educational_details.txt')
file_path_to_job_categories = os.path.join(module_dir,'../static/text/job_categories.txt')
file_path_to_courses = os.path.join(module_dir,'../static/text/courses.txt')

file = open(file_path,"r")
cities=file.readlines()
file.close()
new_cities=[]
for city in cities:
    new_cities.append(city.replace("\n",""))

new_city_1=[]
for city in new_cities:
    new_city_1.append((city,city))

file = open(file_path_to_educational_details,"r")
edu_details = file.readlines()
file.close()
new_edu_details = []
for course in edu_details:
    new_edu_details.append(course.replace("\n",""))
new_edu_details_1 = []
for course in new_edu_details:
    new_edu_details_1.append((course,course))


file = open(file_path_to_job_categories,"r")
job_categories = file.readlines()
file.close()
new_job_categories = []
for job in job_categories:
    new_job_categories.append(job.replace("\n",""))
new_job_categories_1 = []
for job in new_job_categories:
    new_job_categories_1.append((job,job))


#courses
file = open(file_path_to_courses,"r")
courses = file.readlines()
file.close()
new_courses = []
for course in courses:
    new_courses.append(course.replace("\n",""))
new_courses_1 = []
for course in new_courses:
    new_courses_1.append((course,course))