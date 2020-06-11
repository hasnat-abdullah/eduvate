from django.db import models
from datetime import datetime
from instructorApp.models import Country
from courseApp.models import Course,CourseModule
from paymentApp.models import Payment
from eduvate import settings


class Student(models.Model):
    name = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField()
    details = models.TextField(max_length=250)
    city = models.TextField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    image = models.ImageField(default='default', upload_to='image/pro_pics', blank=True)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name.display_name


class StudentWorkHistory(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=60)
    designation = models.CharField(max_length=60)
    start_date = models.DateField(default=datetime.now, blank=False)
    end_date = models.DateField(default=None, blank=True)

    def __str__(self):
        return self.student_id.name.display_name+","+self.designation


ENROLMENT_STATUS_CHOICES = (
        ('completed', 'COMPLETED'),
        ('partial', 'PARTIAL'),
        ('ongoing', 'ONGOING'),
        ('notStarted', 'NOTSTARTED')
    )


class EnrolledCourse(models.Model):
    student_id = models.ManyToManyField(Student)
    course_id = models.ManyToManyField(Course)
    enrolment_status = models.CharField(max_length=10, choices=ENROLMENT_STATUS_CHOICES, default='bkash')
    enrolled_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.course_id.name + " - " + self.student_id.name.username


class EnrolledModule(models.Model):
    enrolled_id = models.ManyToManyField(EnrolledCourse)
    module_id = models.ManyToManyField(CourseModule)
    payment_status= models.ForeignKey(Payment, on_delete=models.PROTECT)
    enrolled_module_on = models.DateField(auto_now=False, auto_now_add=True)
    last_visited_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.module_id.name + " - " + self.enrolled_id.name
