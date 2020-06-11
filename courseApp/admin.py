from django.contrib import admin
from courseApp.models import Language,Category,CourseLevel, Course,CourseInstructor,LearningPath,PathCourse,CourseModule,Lesson

admin.site.register(Course)
admin.site.register(CourseInstructor)
admin.site.register(Lesson)
admin.site.register(Category)
admin.site.register(CourseLevel)
admin.site.register(Language)
admin.site.register(LearningPath)
admin.site.register(PathCourse)
admin.site.register(CourseModule)
