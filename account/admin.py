from django.contrib import admin

from account.models import User, Role, Project, UserData, Permission

admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Project)
admin.site.register(UserData)