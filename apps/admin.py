from django.contrib import admin

# Register your models here.
from apps.models import UserInfo, Employee
from apps.models import Student,Book,Press,Author,AuthorDetail,Students,Classes

admin.site.register(Students)
admin.site.register(Classes)
admin.site.register(UserInfo)
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Book)
admin.site.register(Press)
admin.site.register(Author)
admin.site.register(AuthorDetail)


