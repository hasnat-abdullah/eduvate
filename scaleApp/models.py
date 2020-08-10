from django.db import models
from instructorApp.models import Instructor


class MeasuringScale(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


class QuestionDetails:
    ANSWER_CHOICES = (
        ('0', 'কখনোই না'),
        ('1', 'অনেকাংশে না'),
        ('2', 'মাঝে মাঝে'),
        ('3', 'প্রায়শই'),
        ('4', 'ঘনঘন'),
    )
    scale_id= models.ForeignKey(MeasuringScale, on_delete=models.CASCADE)
    serial = models.AutoField()
    question = models.CharField(max_length=800, null=False)
    answer = models.CharField(max_length=15,choices=ANSWER_CHOICES,default=None)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.scale_id.name +": "+ self.question