from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from eduvate import settings
from ckeditor_uploader.fields import RichTextUploadingField


class Country(models.Model):
    name = models.CharField(max_length=35, null=False)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    details = RichTextUploadingField()
    city = models.TextField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    image = models.ImageField(default='default', upload_to='image/pro_pics', blank=True)
    fb_url = models.URLField()
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name.username


class InstructorWorkHistory(models.Model):
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=60)
    designation = models.CharField(max_length=60)
    start_date = models.DateField(default=datetime.now, blank=False)
    end_date = models.DateField(default=None, blank=True)

    def __str__(self):
        return self.instructor_id.name.username+","+self.designation


class InstructorRating (models.Model):
    instructor_id = models.OneToOneField(Instructor, on_delete=models.CASCADE)
    rating_count = models.PositiveSmallIntegerField (default=0)
    rating_total_value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.instructor_id.name.username + "-"+str(self.rating_count)
