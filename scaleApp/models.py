from django.db import models
from instructorApp.models import Instructor


class MeasuringScale(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


class QuestionDetails(models.Model):
    scale_id= models.ForeignKey(MeasuringScale, on_delete=models.CASCADE)
    serial = models.SmallIntegerField(null=False, default=1)
    question = models.CharField(max_length=800, null=False)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.scale_id.name +": "+ self.question


class AnswerDetails(models.Model):
    scale_id= models.ForeignKey(MeasuringScale, on_delete=models.CASCADE)
    choice = models.CharField(max_length=30,null=False)
    serial = models.SmallIntegerField(null=False, default=1)
    value = models.SmallIntegerField(null=False, default=1)

    def __str__(self):
        return self.scale_id.name +": "+ self.choice