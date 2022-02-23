from django.contrib import admin

from django.contrib.auth.admin import *

from .models import UserDataMeta

# Register your models here.

admin.site.register(UserDataMeta, UserAdmin)
