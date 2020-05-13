from django.contrib import admin

# Register your models here.
from apps.models import UserInfo, Employee
from apps.models import Student

admin.site.register(UserInfo)
admin.site.register(Student)
admin.site.register(Employee)
