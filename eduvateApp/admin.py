from django.contrib import admin
from eduvateApp.models import *

admin.site.register(SlotList)
admin.site.register(Booking)

admin.site.register(Course)
admin.site.register(CourseInstructor)
admin.site.register(Lesson)
admin.site.register(LessonScale)
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

class StudentModel(admin.ModelAdmin):
    list_display = ["__str__", "age","gender","address","education","ocupation","religion","marial_status","socio_economic_status","mental_problem","mental_treatment_type","medicine_taken_duration","physical_problem","knowing_source","created_on"]
    search_fields = ["__str__", "age","gender","address","education","ocupation","religion","marial_status","socio_economic_status","mental_problem","mental_treatment_type","medicine_taken_duration","physical_problem","knowing_source","created_on"]
    class Meta:
        Model = Student
admin.site.register(Student, StudentModel)

class EnrolledCourseModel(admin.ModelAdmin):
    list_display = ["course_id.name","__str__", "enrolment_status","percent_complited","enrolled_on","enrolled_on"]
    search_fields = ["course_id.name","__str__", "enrolment_status","percent_complited","enrolled_on","enrolled_on"]
    class Meta:
        Model = EnrolledCourse
admin.site.register(EnrolledCourse,EnrolledCourseModel)
admin.site.register(EnrolledModule)
admin.site.register(StudentWorkHistory)
admin.site.register(CompletedLesson)
admin.site.register(CompletedCourse)

class MeasuringScaleForModuleResultModel(admin.ModelAdmin):
    list_display = ["__str__", "scale_name.name","totalMarks","result","created_on"]
    search_fields = ["__str__", "scale_name.name","totalMarks","result","created_on"]
    class Meta:
        Model = MeasuringScaleForModuleResult
admin.site.register(MeasuringScaleForModuleResult,MeasuringScaleForModuleResultModel)
