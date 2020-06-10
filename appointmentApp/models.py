from django.db import models
from studentApp.models import Student
from instructorApp.models import Instructor
from datetime import datetime

DAY_CHOICES = (
        ('saturday', 'SATURDAY'),
        ('sunday', 'SUNDAY'),
        ('monday', 'MONDAY'),
        ('tuesday', 'TUESDAY'),
        ('wednesday', 'WEDNESDAY'),
        ('thursday', 'THURSDAY'),
        ('Friday', 'FRIDAY')
    )


class SlotList(models.Model):
    counselor = models.ManyToManyField(Instructor)
    from_time = models.TimeField(default=None)
    to_time = models.TimeField(default=None)
    day = models.CharField(max_length=9, choices=DAY_CHOICES, default='saturday')

    def __str__(self):
        return self.counselor.name.username+"; "+ self.day + ": " + self.from_time +"-"+self.to_time


class Booking (models.Model):
    booked_by=models.ForeignKey(Student, on_delete=models.PROTECT)
    slot_id = models.ForeignKey(SlotList, on_delete=models.PROTECT)
    booking_date = models.DateField(default=datetime.today)
    note = models.CharField(max_length=150)

    def __str__(self):
        return self.counselor.name.username+"; "+ self.booking_date + ": " + self.slot_id.from_time +"-"+self.slot_id.to_time
