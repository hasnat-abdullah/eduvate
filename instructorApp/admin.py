from django.contrib import admin
from instructorApp.models import Country,Instructor,InstructorWorkHistory,InstructorRating

admin.site.register(Country)
admin.site.register(Instructor)
admin.site.register(InstructorWorkHistory)
admin.site.register(InstructorRating)