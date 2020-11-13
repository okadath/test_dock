from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from user_account.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.sessions.models import Session


admin.site.register(License)
# admin.site.register(Code)
admin.site.register(Session)
admin.site.register(LoggedInUser)



class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_class = UserResource


admin.site.unregister(User)
admin.site.register(User, UserAdmin)