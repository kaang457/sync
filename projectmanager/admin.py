from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *


admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Client)
admin.site.register(User, UserAdmin)
