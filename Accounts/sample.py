import os
module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, '../static/text/cities.txt')

file = open(file_path,"r")
cities=file.readlines()
file.close()
new_cities=[]
for city in cities:
    new_cities.append(city.replace("\n",""))

new_city_1=[]
for city in new_cities:
    new_city_1.append((city,city))

