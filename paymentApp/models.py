from django.db import models
from django.contrib.auth.models import User
from courseApp.models import CourseModule
from eduvate import settings

PAYMENT_STATUS_CHOICES = (
        ('completed', 'COMPLETED'),
        ('partial', 'PARTIAL'),
        ('cancel', 'CANCEL'),
        ('hold', 'HOLD'),
        ('pending', 'pending'),
        ('incomplete', 'INCOMPLETE'),
        ('refund', 'REFUND')
    )

PAYMENT_METHOD_CHOICE= (
        ('bkash', 'BKASH'),
        ('rocket', 'ROCKET')
    )


class Payment(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    paid_for_module= models.ForeignKey(CourseModule, on_delete=models.PROTECT)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHOD_CHOICE, default='bkash')
    paid_amount = models.DecimalField(max_digits=8 ,decimal_places=2)
    txn_id = models.CharField(max_length=20)
    reference = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='incomplete')

    def __str__(self):
        return self.user_id.username+","+self.payment_method +"-"+ self.paid_amount +"tk -"+ self.txn_id