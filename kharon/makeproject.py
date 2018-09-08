import os
from pkg_resources import resource_filename, Requirement
from shutil import copyfile

template_path = resource_filename(Requirement.parse("kharon"), "kharon/projecttemplates/")
template_files = os.listdir(template_path)

for filename in template_files:
    if not filename in ['__init__.py', '__pycache__']:
        print(template_path+filename)
        copyfile(template_path+filename, os.getcwd()+"/"+filename)
