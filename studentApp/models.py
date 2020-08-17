from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from instructorApp.models import Country
from courseApp.models import Course, CourseModule
from paymentApp.models import Payment
from scaleApp.models import MeasuringScale
from datetime import datetime
from eduvate import settings


class StudentManager(models.Manager):
    def create_student(self, username,age,city,country):
        student = self.create(name=username,age=age,city=city,country=country)
        return student


class Student(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField()
    city = models.TextField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name.username

    objects = StudentManager()


class StudentWorkHistory(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=60)
    designation = models.CharField(max_length=60)
    start_date = models.DateField(default=datetime.now, blank=False)
    end_date = models.DateField(default=None, blank=True)

    def __str__(self):
        return self.student_id.name.username+","+self.designation


ENROLMENT_STATUS_CHOICES = (
        ('completed', 'COMPLETED'),
        ('partial', 'PARTIAL'),
        ('ongoing', 'ONGOING'),
        ('notStarted', 'NOTSTARTED')
    )


class EnrolledCourse(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolment_status = models.CharField(max_length=10, choices=ENROLMENT_STATUS_CHOICES, default='ongoing')
    enrolled_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.course_id.name + " - " + self.student_id.name.username


class EnrolledModule(models.Model):
    enrolled_id = models.ForeignKey(EnrolledCourse, on_delete=models.CASCADE)
    module_id = models.ForeignKey(CourseModule,models.CASCADE)
    payment_status= models.ForeignKey(Payment, on_delete=models.PROTECT)
    enrolled_module_on = models.DateField(auto_now=False, auto_now_add=True)
    last_visited_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.module_id.name + " - " + self.enrolled_id.course_id.name


class ScoreManager(models.Manager):
    def create_score(self, username, scale_name, totalMarks):
        studentScore = self.create(user_id=username,scale_name=scale_name,totalMarks=totalMarks,created_on=datetime.now)
        return studentScore


class MeasuringScaleForModuleResult(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    scale_name = models.ForeignKey(MeasuringScale, on_delete=models.CASCADE)
    totalMarks = models.PositiveSmallIntegerField()
    created_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user_id.username +": "+ str(self.created_on)

    objects=ScoreManager()