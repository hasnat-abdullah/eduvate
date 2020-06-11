from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from datetime import datetime
from eduvate import settings


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    display_name = models.CharField(max_length=140)
    date_joined = models.DateTimeField(default=datetime.now)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ["display_name",]

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_name(self):
        return self.display_name

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        first_name = self.display_name.split()[0]
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Country(models.Model):
    name = models.CharField(max_length=35, null=False)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    name = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    details = models.TextField(max_length=250)
    city = models.TextField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    image = models.ImageField(default='default', upload_to='image/pro_pics', blank=True)

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
        return self.instructor_id.name.username + "-"+self.rating_count
