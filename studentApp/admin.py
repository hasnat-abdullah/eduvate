from django.contrib import admin
from studentApp.models import Student, StudentWorkHistory,EnrolledCourse,EnrolledModule

admin.site.register(Student)
admin.site.register(EnrolledCourse)
admin.site.register(EnrolledModule)
admin.site.register(StudentWorkHistory)
