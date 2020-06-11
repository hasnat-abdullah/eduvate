from django.contrib import admin
from instructorApp.models import User,Country,Instructor,InstructorWorkHistory,InstructorRating

admin.site.register(User)
admin.site.register(Country)
admin.site.register(Instructor)
admin.site.register(InstructorWorkHistory)
admin.site.register(InstructorRating)