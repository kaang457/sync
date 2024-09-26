import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()

from projectmanager.models import *

project = Project.objects.get(name="Main Project 1")

print(project.pk)
