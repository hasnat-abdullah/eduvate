from django.contrib import admin
from eduvateApp.models import *

admin.site.register(SlotList)
admin.site.register(Booking)

admin.site.register(Course)
admin.site.register(CourseInstructor)
admin.site.register(Lesson)
admin.site.register(Category)
admin.site.register(CourseLevel)
admin.site.register(Language)
admin.site.register(LearningPath)
admin.site.register(PathCourse)
admin.site.register(CourseModule)

admin.site.register(Country)
admin.site.register(Instructor)
admin.site.register(InstructorWorkHistory)
admin.site.register(InstructorRating)

admin.site.register(Payment)

admin.site.register(MeasuringScale)
admin.site.register(QuestionDetails)
admin.site.register(AnswerDetails)
admin.site.register(ScoringDetails)

admin.site.register(Student)
admin.site.register(EnrolledCourse)
admin.site.register(EnrolledModule)
admin.site.register(StudentWorkHistory)
admin.site.register(CompletedLesson)
admin.site.register(CompletedCourse)

