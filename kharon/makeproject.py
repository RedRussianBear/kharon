import os
from pkg_resources import resource_filename, Requirement

template_files = os.listdir(resource_filename(Requirement.parse("kharon"), "kharon/projecttemplates/"))

print(template_files)